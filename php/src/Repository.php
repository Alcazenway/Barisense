<?php

declare(strict_types=1);

require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/Storage.php';
require_once __DIR__ . '/analysis.php';

class Repository
{
    public function __construct(private Storage $storage)
    {
    }

    // Coffees
    public function listCoffees(): array
    {
        $coffees = $this->storage->all('coffees');
        usort($coffees, fn($a, $b) => strcmp($b['created_at'], $a['created_at']));
        return $coffees;
    }

    public function getCoffee(string $id): ?array
    {
        foreach ($this->storage->all('coffees') as $coffee) {
            if ($coffee['id'] === $id) {
                return $coffee;
            }
        }
        return null;
    }

    public function upsertCoffee(array $payload, ?string $id = null): array
    {
        $coffees = $this->storage->all('coffees');
        $now = now_iso();
        $found = false;
        foreach ($coffees as &$coffee) {
            if ($coffee['id'] === $id) {
                $coffee = array_merge($coffee, $payload);
                $coffee['cost_per_shot_eur'] = compute_cost_per_shot((float) $coffee['price_eur'], (int) $coffee['weight_grams']);
                $found = true;
            }
        }
        unset($coffee);
        if (!$found) {
            $payload['id'] = uuidv4();
            $payload['created_at'] = $now;
            $payload['cost_per_shot_eur'] = compute_cost_per_shot((float) $payload['price_eur'], (int) $payload['weight_grams']);
            $coffees[] = $payload;
        }
        $this->storage->set('coffees', $coffees);
        return $found ? $this->getCoffee($id) : end($coffees);
    }

    public function deleteCoffee(string $id): void
    {
        $coffees = array_values(array_filter($this->storage->all('coffees'), fn($c) => $c['id'] !== $id));
        $shots = $this->storage->all('shots');
        $tastings = $this->storage->all('tastings');
        $verdicts = $this->storage->all('verdicts');

        $shots = array_values(array_filter($shots, fn($shot) => $shot['coffee_id'] !== $id));
        $shotIds = array_column($shots, 'id');
        $tastings = array_values(array_filter($tastings, fn($tasting) => in_array($tasting['shot_id'], $shotIds, true)));
        $verdicts = array_values(array_filter($verdicts, fn($verdict) => $verdict['coffee_id'] !== $id));

        $this->storage->set('coffees', $coffees);
        $this->storage->set('shots', $shots);
        $this->storage->set('tastings', $tastings);
        $this->storage->set('verdicts', $verdicts);
    }

    // Waters
    public function listWaters(): array
    {
        $waters = $this->storage->all('waters');
        usort($waters, fn($a, $b) => strcmp($b['created_at'], $a['created_at']));
        return $waters;
    }

    public function getWater(string $id): ?array
    {
        foreach ($this->storage->all('waters') as $water) {
            if ($water['id'] === $id) {
                return $water;
            }
        }
        return null;
    }

    public function upsertWater(array $payload, ?string $id = null): array
    {
        $waters = $this->storage->all('waters');
        $now = now_iso();
        $found = false;
        foreach ($waters as &$water) {
            if ($water['id'] === $id) {
                $water = array_merge($water, $payload);
                $found = true;
            }
        }
        unset($water);
        if (!$found) {
            $payload['id'] = uuidv4();
            $payload['created_at'] = $now;
            $waters[] = $payload;
        }
        $this->storage->set('waters', $waters);
        return $found ? $this->getWater($id) : end($waters);
    }

    public function deleteWater(string $id): void
    {
        $waters = array_values(array_filter($this->storage->all('waters'), fn($w) => $w['id'] !== $id));
        $this->storage->set('waters', $waters);
    }

    // Shots
    public function listShots(): array
    {
        $shots = $this->storage->all('shots');
        usort($shots, fn($a, $b) => strcmp($b['created_at'], $a['created_at']));
        return $shots;
    }

    public function getShot(string $id): ?array
    {
        foreach ($this->storage->all('shots') as $shot) {
            if ($shot['id'] === $id) {
                return $shot;
            }
        }
        return null;
    }

    public function listShotsForCoffee(string $coffeeId): array
    {
        return array_values(array_filter($this->storage->all('shots'), fn($s) => $s['coffee_id'] === $coffeeId));
    }

    public function addShot(array $payload): array
    {
        if (!$this->getCoffee($payload['coffee_id'])) {
            throw new InvalidArgumentException('coffee_not_found');
        }
        if (!empty($payload['water_id']) && !$this->getWater($payload['water_id'])) {
            throw new InvalidArgumentException('water_not_found');
        }
        $shot = $payload;
        $shot['id'] = uuidv4();
        $shot['created_at'] = now_iso();
        $shot['brew_ratio'] = compute_brew_ratio((float) $payload['beverage_weight_grams'], (float) $payload['dose_in_grams']);
        $shots = $this->storage->all('shots');
        $shots[] = $shot;
        $this->storage->set('shots', $shots);
        return $shot;
    }

    public function updateShot(string $id, array $payload): array
    {
        $shots = $this->storage->all('shots');
        $found = false;
        foreach ($shots as &$shot) {
            if ($shot['id'] === $id) {
                if (!$this->getCoffee($payload['coffee_id'])) {
                    throw new InvalidArgumentException('coffee_not_found');
                }
                if (!empty($payload['water_id']) && !$this->getWater($payload['water_id'])) {
                    throw new InvalidArgumentException('water_not_found');
                }
                $shot = array_merge($shot, $payload);
                $shot['brew_ratio'] = compute_brew_ratio((float) $payload['beverage_weight_grams'], (float) $payload['dose_in_grams']);
                $found = true;
            }
        }
        unset($shot);
        if (!$found) {
            throw new InvalidArgumentException('shot_not_found');
        }
        $this->storage->set('shots', $shots);
        return $this->getShot($id);
    }

    public function deleteShot(string $id): void
    {
        $shots = array_values(array_filter($this->storage->all('shots'), fn($s) => $s['id'] !== $id));
        $tastings = array_values(array_filter($this->storage->all('tastings'), fn($t) => $t['shot_id'] !== $id));
        $this->storage->set('shots', $shots);
        $this->storage->set('tastings', $tastings);
    }

    // Tastings
    public function listTastings(): array
    {
        $tastings = $this->storage->all('tastings');
        usort($tastings, fn($a, $b) => strcmp($b['created_at'], $a['created_at']));
        return $tastings;
    }

    public function getTasting(string $id): ?array
    {
        foreach ($this->storage->all('tastings') as $t) {
            if ($t['id'] === $id) {
                return $t;
            }
        }
        return null;
    }

    public function addTasting(array $payload): array
    {
        $shot = $this->getShot($payload['shot_id']);
        if (!$shot) {
            throw new InvalidArgumentException('shot_not_found');
        }
        $scores = labels_to_scores($payload);
        $mean = compute_sensory_mean(array_values($scores));
        $tasting = [
            'id' => uuidv4(),
            'shot_id' => $payload['shot_id'],
            'created_at' => now_iso(),
            'comments' => $payload['comments'] ?? null,
            'acidity_label' => $payload['acidity_label'],
            'bitterness_label' => $payload['bitterness_label'],
            'body_label' => $payload['body_label'],
            'aroma_label' => $payload['aroma_label'],
            'balance_label' => $payload['balance_label'],
            'finish_label' => $payload['finish_label'],
            'overall_label' => $payload['overall_label'],
            'sensory_mean' => $mean,
        ];
        $tastings = $this->storage->all('tastings');
        $tastings[] = $tasting;
        $this->storage->set('tastings', $tastings);

        $status = verdict_from_mean($mean);
        $rationale = 'Moyenne sensorielle ' . mean_to_label($mean) . ' sur le dernier shot';
        $this->upsertVerdict([
            'coffee_id' => $shot['coffee_id'],
            'status' => $status,
            'rationale' => $rationale,
        ]);

        return $tasting;
    }

    public function deleteTasting(string $id): void
    {
        $tastings = array_values(array_filter($this->storage->all('tastings'), fn($t) => $t['id'] !== $id));
        $this->storage->set('tastings', $tastings);
    }

    // Verdicts
    public function listVerdicts(): array
    {
        return $this->storage->all('verdicts');
    }

    public function getVerdict(string $id): ?array
    {
        foreach ($this->storage->all('verdicts') as $verdict) {
            if ($verdict['id'] === $id) {
                return $verdict;
            }
        }
        return null;
    }

    public function upsertVerdict(array $payload, ?string $id = null): array
    {
        $verdicts = $this->storage->all('verdicts');
        $now = now_iso();
        $found = false;
        if ($id) {
            foreach ($verdicts as &$verdict) {
                if ($verdict['id'] === $id) {
                    $verdict = array_merge($verdict, $payload);
                    $found = true;
                }
            }
            unset($verdict);
        }
        if (!$found) {
            foreach ($verdicts as &$verdict) {
                if ($verdict['coffee_id'] === $payload['coffee_id']) {
                    $verdict = array_merge($verdict, $payload);
                    $found = true;
                }
            }
            unset($verdict);
        }
        if (!$found) {
            $payload['id'] = uuidv4();
            $payload['created_at'] = $now;
            $verdicts[] = $payload;
        }
        $this->storage->set('verdicts', $verdicts);
        return $found ? ($id ? $this->getVerdict($id) : $this->findVerdictByCoffee($payload['coffee_id'])) : end($verdicts);
    }

    public function deleteVerdict(string $id): void
    {
        $verdicts = array_values(array_filter($this->storage->all('verdicts'), fn($v) => $v['id'] !== $id));
        $this->storage->set('verdicts', $verdicts);
    }

    public function findVerdictByCoffee(string $coffeeId): ?array
    {
        foreach ($this->storage->all('verdicts') as $verdict) {
            if ($verdict['coffee_id'] === $coffeeId) {
                return $verdict;
            }
        }
        return null;
    }

    // Analytics helpers
    public function tastingsByCoffee(string $coffeeId): array
    {
        $shots = $this->listShotsForCoffee($coffeeId);
        $shotIds = array_column($shots, 'id');
        return array_values(array_filter($this->storage->all('tastings'), fn($t) => in_array($t['shot_id'], $shotIds, true)));
    }

    public function tastingCounts(): array
    {
        $counts = [];
        foreach ($this->listCoffees() as $coffee) {
            $counts[$coffee['id']] = 0;
        }
        foreach ($this->storage->all('tastings') as $tasting) {
            $shot = $this->getShot($tasting['shot_id']);
            if ($shot) {
                $counts[$shot['coffee_id']] = ($counts[$shot['coffee_id']] ?? 0) + 1;
            }
        }
        return $counts;
    }
}
