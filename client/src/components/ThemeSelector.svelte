<script lang="ts">
    import { onMount } from 'svelte';

    interface Theme {
        VALUE: string;
        LABEL: string;
        EMOJI: string;
    }

    const THEMES: Theme[] = [
        { VALUE: 'default', LABEL: 'Default', EMOJI: '🎨' },
        { VALUE: 'retro', LABEL: '80s Retro', EMOJI: '🕹️' },
        { VALUE: 'terminal', LABEL: 'Terminal Classic', EMOJI: '💻' },
        { VALUE: 'sketched', LABEL: 'Hand-Sketched', EMOJI: '✏️' },
        { VALUE: 'steampunk', LABEL: 'Steampunk', EMOJI: '⚙️' },
        { VALUE: 'fantasy', LABEL: 'Fantasy Realm', EMOJI: '🧙' },
    ];

    let CURRENT_THEME = '';

    const APPLY_THEME = (THEME: string) => {
        document.documentElement.setAttribute('data-theme', THEME);
        localStorage.setItem('selected-theme', THEME);
        CURRENT_THEME = THEME;
    };

    const ON_THEME_CHANGE = (EVENT: Event) => {
        const TARGET = EVENT.target as HTMLSelectElement;
        APPLY_THEME(TARGET.value);
    };

    onMount(() => {
        const SAVED_THEME = localStorage.getItem('selected-theme') || 'default';
        APPLY_THEME(SAVED_THEME);
    });
</script>

<div class="theme-selector-wrapper flex items-center gap-2">
    <label for="theme-select" class="theme-label text-sm font-medium opacity-80 whitespace-nowrap">Theme:</label>
    <select
        id="theme-select"
        value={CURRENT_THEME}
        on:change={ON_THEME_CHANGE}
        class="theme-select text-sm rounded-lg px-3 py-1.5 border focus:outline-none focus:ring-2 transition-all duration-300 cursor-pointer"
        aria-label="Select website theme"
    >
        {#each THEMES as THEME (THEME.VALUE)}
            <option value={THEME.VALUE}>{THEME.EMOJI} {THEME.LABEL}</option>
        {/each}
    </select>
</div>

<style>
    .theme-select {
        background-color: var(--theme-select-bg, rgba(255,255,255,0.15));
        color: var(--theme-select-text, #ffffff);
        border-color: var(--theme-select-border, rgba(255,255,255,0.3));
    }

    .theme-select:focus {
        ring-color: var(--theme-accent, #60a5fa);
    }

    .theme-select option {
        background-color: var(--theme-option-bg, #1e293b);
        color: var(--theme-option-text, #f1f5f9);
    }
</style>
