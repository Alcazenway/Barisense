<?php

declare(strict_types=1);

class Storage
{
    private string $file;
    private array $data = [
        'coffees' => [],
        'waters' => [],
        'shots' => [],
        'tastings' => [],
        'verdicts' => [],
    ];

    public function __construct(string $file)
    {
        $this->file = $file;
        $this->load();
    }

    public function all(string $key): array
    {
        return $this->data[$key] ?? [];
    }

    public function set(string $key, array $value): void
    {
        $this->data[$key] = $value;
        $this->persist();
    }

    private function load(): void
    {
        if (!file_exists($this->file)) {
            $this->persist();
            return;
        }
        $content = file_get_contents($this->file);
        if ($content === false || $content === '') {
            $this->persist();
            return;
        }
        $decoded = json_decode($content, true);
        if (is_array($decoded)) {
            $this->data = array_merge($this->data, $decoded);
        }
    }

    private function persist(): void
    {
        $dir = dirname($this->file);
        if (!is_dir($dir)) {
            mkdir($dir, 0775, true);
        }
        file_put_contents($this->file, json_encode($this->data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    }
}
