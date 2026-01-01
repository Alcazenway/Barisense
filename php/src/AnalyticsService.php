<?php

declare(strict_types=1);

require_once __DIR__ . '/analysis.php';
require_once __DIR__ . '/Repository.php';

class AnalyticsService
{
    public function __construct(private Repository $repository)
    {
    }

    private function averageForCoffee(string $coffeeId, ?string $beverage = null): ?float
    {
        $tastings = $this->repository->tastingsByCoffee($coffeeId);
        if ($beverage) {
            $shots = array_filter($this->repository->listShotsForCoffee($coffeeId), fn($s) => $s['beverage_type'] === $beverage);
            $shotIds = array_column($shots, 'id');
            $tastings = array_filter($tastings, fn($t) => in_array($t['shot_id'], $shotIds, true));
        }
        if (!$tastings) {
            return null;
        }
        $scores = array_map(fn($t) => $t['sensory_mean'], $tastings);
        return array_sum($scores) / count($scores);
    }

    private function verdictLabel(string $coffeeId): string
    {
        $verdict = $this->repository->findVerdictByCoffee($coffeeId);
        if ($verdict) {
            return verdict_label($verdict['status']);
        }
        $avg = $this->averageForCoffee($coffeeId);
        if ($avg === null) {
            return 'en observation';
        }
        return verdict_label(verdict_from_mean($avg));
    }

    public function ranking(?string $beverage = null): array
    {
        $means = [];
        foreach ($this->repository->listCoffees() as $coffee) {
            $avg = $this->averageForCoffee($coffee['id'], $beverage);
            if ($avg !== null) {
                $means[$coffee['id']] = ['coffee' => $coffee, 'mean' => $avg];
            }
        }
        $ranking = summarize_rankings($means);
        $label = $beverage;
        return array_map(function ($item) use ($label) {
            [$position, $coffeeId, $data] = $item;
            return [
                'position' => $position,
                'coffee_id' => $coffeeId,
                'name' => $data['coffee']['name'],
                'roaster' => $data['coffee']['roaster'],
                'score_label' => mean_to_label($data['mean']),
                'verdict_label' => $this->verdictLabel($coffeeId),
                'beverage_filter' => $label,
            ];
        }, $ranking);
    }

    public function qualityPrice(): array
    {
        $insights = [];
        $priority = [
            'excellent rapport Q/P' => 4,
            'bon rapport Q/P' => 3,
            'moyen' => 2,
            'défavorable' => 1,
            'non renseigné' => 0,
        ];
        foreach ($this->repository->listCoffees() as $coffee) {
            $avg = $this->averageForCoffee($coffee['id']);
            if ($avg === null) {
                continue;
            }
            $ratio = aggregate_quality_per_price($avg, (float) $coffee['cost_per_shot_eur']);
            $insights[] = [
                'coffee_id' => $coffee['id'],
                'name' => $coffee['name'],
                'roaster' => $coffee['roaster'],
                'cost_per_shot_eur' => $coffee['cost_per_shot_eur'],
                'quality_label' => mean_to_label($avg),
                'verdict_label' => $this->verdictLabel($coffee['id']),
                'ratio_label' => $ratio,
            ];
        }
        usort($insights, fn($a, $b) => ($priority[$b['ratio_label']] ?? 0) <=> ($priority[$a['ratio_label']] ?? 0));
        return $insights;
    }

    public function stability(): array
    {
        $insights = [];
        foreach ($this->repository->listCoffees() as $coffee) {
            $means = array_map(fn($t) => $t['sensory_mean'], $this->repository->tastingsByCoffee($coffee['id']));
            if (!$means) {
                continue;
            }
            $insights[] = [
                'coffee_id' => $coffee['id'],
                'name' => $coffee['name'],
                'roaster' => $coffee['roaster'],
                'stability' => stability_label($means),
                'sample_size' => count($means),
            ];
        }
        return $insights;
    }

    public function retest(): array
    {
        $counts = $this->repository->tastingCounts();
        $candidates = summarize_retest_needed($counts);
        $coffees = array_filter($this->repository->listCoffees(), fn($c) => in_array($c['id'], $candidates, true));
        return array_map(fn($c) => [
            'coffee_id' => $c['id'],
            'name' => $c['name'],
            'roaster' => $c['roaster'],
            'reason' => 'Une seule dégustation ou aucune',
        ], $coffees);
    }
}
