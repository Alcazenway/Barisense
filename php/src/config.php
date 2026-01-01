<?php

return [
    'api_prefix' => '/api/v1',
    'health_path' => '/api/health',
    'api_key_header' => 'X-API-Key',
    'api_key' => null, // définir une valeur pour activer la protection
    'storage_file' => __DIR__ . '/../storage/data.json',
];
