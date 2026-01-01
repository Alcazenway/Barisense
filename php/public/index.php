<?php

declare(strict_types=1);

$config = require __DIR__ . '/../src/config.php';
require_once __DIR__ . '/../src/helpers.php';
require_once __DIR__ . '/../src/Storage.php';
require_once __DIR__ . '/../src/Repository.php';
require_once __DIR__ . '/../src/AnalyticsService.php';

$method = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);

if ($method === 'OPTIONS') {
    send_json(['status' => 'ok']);
}

if ($path === $config['health_path']) {
    send_json(['status' => 'ok', 'timestamp' => now_iso()]);
}

if (!str_starts_with($path, $config['api_prefix'])) {
    not_found('Route inconnue');
}

if ($config['api_key'] !== null) {
    $header = 'HTTP_' . strtoupper(str_replace('-', '_', $config['api_key_header']));
    $provided = $_SERVER[$header] ?? null;
    if ($provided !== $config['api_key']) {
        unauthorized();
    }
}

$storage = new Storage($config['storage_file']);
$repository = new Repository($storage);
$analytics = new AnalyticsService($repository);

$trimmed = substr($path, strlen($config['api_prefix']));
$segments = array_values(array_filter(explode('/', $trimmed)));
$resource = $segments[0] ?? '';
$identifier = $segments[1] ?? null;
$sub = $segments[2] ?? null;

switch ($resource) {
    case 'coffees':
        handleCoffees($method, $identifier, $repository);
        break;
    case 'waters':
        handleWaters($method, $identifier, $repository);
        break;
    case 'shots':
        handleShots($method, $identifier, $repository);
        break;
    case 'tastings':
        handleTastings($method, $identifier, $repository);
        break;
    case 'verdicts':
        handleVerdicts($method, $identifier, $repository);
        break;
    case 'analytics':
        handleAnalytics($method, $identifier, $sub, $analytics);
        break;
    default:
        not_found('Route inconnue');
}

function handleCoffees(string $method, ?string $id, Repository $repository): void
{
    switch ($method) {
        case 'GET':
            if ($id) {
                $coffee = $repository->getCoffee($id);
                $coffee ? send_json($coffee) : not_found('Café introuvable');
            } else {
                send_json($repository->listCoffees());
            }
            break;
        case 'POST':
            $payload = read_json_body();
            validatePayload($payload, ['name', 'roaster', 'format', 'weight_grams', 'price_eur', 'purchased_at']);
            $created = $repository->upsertCoffee($payload);
            send_json($created, 201);
            break;
        case 'PUT':
            if (!$id) {
                bad_request('Identifiant requis');
            }
            if (!$repository->getCoffee($id)) {
                not_found('Café introuvable');
            }
            $payload = read_json_body();
            validatePayload($payload, ['name', 'roaster', 'format', 'weight_grams', 'price_eur', 'purchased_at']);
            $updated = $repository->upsertCoffee($payload, $id);
            send_json($updated);
            break;
        case 'DELETE':
            if (!$id) {
                bad_request('Identifiant requis');
            }
            if (!$repository->getCoffee($id)) {
                not_found('Café introuvable');
            }
            $repository->deleteCoffee($id);
            send_json(['status' => 'deleted']);
            break;
        default:
            method_not_allowed();
    }
}

function handleWaters(string $method, ?string $id, Repository $repository): void
{
    switch ($method) {
        case 'GET':
            if ($id) {
                $water = $repository->getWater($id);
                $water ? send_json($water) : not_found('Eau introuvable');
            } else {
                send_json($repository->listWaters());
            }
            break;
        case 'POST':
            $payload = read_json_body();
            validatePayload($payload, ['label', 'source']);
            $created = $repository->upsertWater($payload);
            send_json($created, 201);
            break;
        case 'PUT':
            if (!$id) {
                bad_request('Identifiant requis');
            }
            if (!$repository->getWater($id)) {
                not_found('Eau introuvable');
            }
            $payload = read_json_body();
            validatePayload($payload, ['label', 'source']);
            $updated = $repository->upsertWater($payload, $id);
            send_json($updated);
            break;
        case 'DELETE':
            if (!$id) {
                bad_request('Identifiant requis');
            }
            $repository->deleteWater($id);
            send_json(['status' => 'deleted']);
            break;
        default:
            method_not_allowed();
    }
}

function handleShots(string $method, ?string $id, Repository $repository): void
{
    switch ($method) {
        case 'GET':
            if ($id) {
                $shot = $repository->getShot($id);
                $shot ? send_json($shot) : not_found('Shot introuvable');
            } else {
                send_json($repository->listShots());
            }
            break;
        case 'POST':
            $payload = read_json_body();
            validatePayload($payload, [
                'coffee_id', 'beverage_type', 'grind_setting', 'dose_in_grams', 'beverage_weight_grams', 'extraction_time_seconds'
            ]);
            try {
                $created = $repository->addShot($payload);
                send_json($created, 201);
            } catch (InvalidArgumentException $e) {
                bad_request($e->getMessage());
            }
            break;
        case 'PUT':
            if (!$id) {
                bad_request('Identifiant requis');
            }
            $payload = read_json_body();
            validatePayload($payload, [
                'coffee_id', 'beverage_type', 'grind_setting', 'dose_in_grams', 'beverage_weight_grams', 'extraction_time_seconds'
            ]);
            try {
                $updated = $repository->updateShot($id, $payload);
                send_json($updated);
            } catch (InvalidArgumentException $e) {
                bad_request($e->getMessage());
            }
            break;
        case 'DELETE':
            if (!$id) {
                bad_request('Identifiant requis');
            }
            $repository->deleteShot($id);
            send_json(['status' => 'deleted']);
            break;
        default:
            method_not_allowed();
    }
}

function handleTastings(string $method, ?string $id, Repository $repository): void
{
    switch ($method) {
        case 'GET':
            if ($id) {
                $tasting = $repository->getTasting($id);
                $tasting ? send_json($tasting) : not_found('Dégustation introuvable');
            } else {
                send_json($repository->listTastings());
            }
            break;
        case 'POST':
            $payload = read_json_body();
            validatePayload($payload, [
                'shot_id', 'acidity_label', 'bitterness_label', 'body_label', 'aroma_label', 'balance_label', 'finish_label', 'overall_label'
            ]);
            try {
                $created = $repository->addTasting($payload);
                send_json($created, 201);
            } catch (InvalidArgumentException $e) {
                bad_request($e->getMessage());
            }
            break;
        case 'DELETE':
            if (!$id) {
                bad_request('Identifiant requis');
            }
            $repository->deleteTasting($id);
            send_json(['status' => 'deleted']);
            break;
        default:
            method_not_allowed();
    }
}

function handleVerdicts(string $method, ?string $id, Repository $repository): void
{
    switch ($method) {
        case 'GET':
            if ($id) {
                $verdict = $repository->getVerdict($id);
                $verdict ? send_json($verdict) : not_found('Verdict introuvable');
            } else {
                send_json($repository->listVerdicts());
            }
            break;
        case 'POST':
            $payload = read_json_body();
            validatePayload($payload, ['coffee_id', 'status']);
            $created = $repository->upsertVerdict($payload);
            send_json($created, 201);
            break;
        case 'PUT':
            if (!$id) {
                bad_request('Identifiant requis');
            }
            $payload = read_json_body();
            validatePayload($payload, ['coffee_id', 'status']);
            $updated = $repository->upsertVerdict($payload, $id);
            send_json($updated);
            break;
        case 'DELETE':
            if (!$id) {
                bad_request('Identifiant requis');
            }
            $repository->deleteVerdict($id);
            send_json(['status' => 'deleted']);
            break;
        default:
            method_not_allowed();
    }
}

function handleAnalytics(string $method, ?string $first, ?string $second, AnalyticsService $service): void
{
    if ($method !== 'GET') {
        method_not_allowed();
    }
    if ($first === 'rankings') {
        $beverage = $second === 'ristretto' ? 'ristretto' : ($second === 'expresso' ? 'expresso' : null);
        if ($second === null) {
            $second = 'global';
        }
        if (!in_array($second, ['global', 'ristretto', 'expresso'], true)) {
            not_found('Classement inconnu');
        }
        $ranking = $service->ranking($beverage);
        send_json($ranking);
    }
    if ($first === 'quality-price') {
        send_json($service->qualityPrice());
    }
    if ($first === 'stability') {
        send_json($service->stability());
    }
    if ($first === 'retest') {
        send_json($service->retest());
    }
    not_found('Route analytique inconnue');
}

function validatePayload(array $payload, array $required): void
{
    $missing = array_filter($required, fn($field) => !array_key_exists($field, $payload));
    if ($missing) {
        bad_request('Champs manquants : ' . implode(', ', $missing));
    }
}
