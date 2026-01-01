<?php

declare(strict_types=1);

require_once __DIR__ . '/helpers.php';

const TARGET_BREW_RATIOS = [
    'ristretto' => 1.6,
    'expresso' => 2.0,
    'cafe_long' => 2.8,
];

const SENSORY_LABEL_TO_SCORE = [
    'insipide' => 1,
    'doux' => 2,
    'équilibré' => 3,
    'equilibre' => 3,
    'expressif' => 4,
    'intense' => 5,
];

function compute_cost_per_shot(float $price, int $weightGrams, float $dose = 18.0): float
{
    if ($weightGrams <= 0) {
        return 0.0;
    }
    $unit = $price / $weightGrams;
    return round($unit * $dose, 2);
}

function compute_brew_ratio(float $beverageWeight, float $dose): float
{
    if ($dose <= 0) {
        return 0.0;
    }
    return round($beverageWeight / $dose, 2);
}

function label_to_score(string $label): int
{
    $normalized = strtolower(trim($label));
    if (!array_key_exists($normalized, SENSORY_LABEL_TO_SCORE)) {
        throw new InvalidArgumentException('unknown_label:' . $label);
    }
    return SENSORY_LABEL_TO_SCORE[$normalized];
}

function labels_to_scores(array $payload): array
{
    return [
        'acidity_score' => label_to_score($payload['acidity_label']),
        'bitterness_score' => label_to_score($payload['bitterness_label']),
        'body_score' => label_to_score($payload['body_label']),
        'aroma_score' => label_to_score($payload['aroma_label']),
        'balance_score' => label_to_score($payload['balance_label']),
        'finish_score' => label_to_score($payload['finish_label']),
        'overall_score' => label_to_score($payload['overall_label']),
    ];
}

function compute_sensory_mean(array $scores): float
{
    if (count($scores) === 0) {
        return 0.0;
    }
    return round(array_sum($scores) / count($scores), 2);
}

function mean_to_label(float $score): string
{
    $rounded = max(1, min(5, (int) round($score)));
    foreach (SENSORY_LABEL_TO_SCORE as $label => $value) {
        if ($value === $rounded) {
            return $label === 'equilibre' ? 'équilibré' : $label;
        }
    }
    return 'équilibré';
}

function verdict_from_mean(float $score): string
{
    if ($score >= 4.5) {
        return 'racheter';
    }
    if ($score >= 3.5) {
        return 'a_affiner';
    }
    if ($score >= 2.5) {
        return 'en_observation';
    }
    return 'a_eviter';
}

function verdict_label(string $status): string
{
    return [
        'racheter' => 'racheter',
        'a_affiner' => 'à affiner',
        'en_observation' => 'en observation',
        'a_eviter' => 'à éviter',
    ][$status] ?? 'en observation';
}

function stability_label(array $scores): string
{
    if (count($scores) < 2) {
        return 'données insuffisantes';
    }
    $mean = array_sum($scores) / count($scores);
    $variance = array_sum(array_map(fn($s) => pow($s - $mean, 2), $scores)) / count($scores);
    $std = sqrt($variance);
    if ($std < 0.25) {
        return 'très stable';
    }
    if ($std < 0.5) {
        return 'assez stable';
    }
    if ($std < 1) {
        return 'variable';
    }
    return 'très variable';
}

function aggregate_quality_per_price(float $avgQuality, float $costPerShot): string
{
    if ($costPerShot <= 0) {
        return 'non renseigné';
    }
    $ratio = $avgQuality / $costPerShot;
    if ($ratio >= 0.2) {
        return 'excellent rapport Q/P';
    }
    if ($ratio >= 0.15) {
        return 'bon rapport Q/P';
    }
    if ($ratio >= 0.1) {
        return 'moyen';
    }
    return 'défavorable';
}

function summarize_rankings(array $means): array
{
    uasort($means, fn($a, $b) => $b['mean'] <=> $a['mean']);
    $result = [];
    $position = 1;
    foreach ($means as $coffeeId => $data) {
        $result[] = [$position, $coffeeId, $data];
        $position++;
    }
    return $result;
}

function summarize_retest_needed(array $counts): array
{
    return array_keys(array_filter($counts, fn($count) => $count < 2));
}
