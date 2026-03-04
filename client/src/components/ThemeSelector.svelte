<script lang="ts">
  import { onMount } from 'svelte';

  const THEMES = [
    { VALUE: 'default', LABEL: 'Default', EMOJI: '🌙' },
    { VALUE: 'retro', LABEL: '80s Retro', EMOJI: '🕹️' },
    { VALUE: 'terminal', LABEL: 'Terminal Classic', EMOJI: '💻' },
    { VALUE: 'sketched', LABEL: 'Hand-Sketched', EMOJI: '✏️' },
    { VALUE: 'steampunk', LABEL: 'Steampunk', EMOJI: '⚙️' },
    { VALUE: 'fantasy', LABEL: 'Fantasy Realm', EMOJI: '🧙' },
  ];

  let CURRENT_THEME = 'default';

  const APPLY_THEME = (THEME_VALUE: string) => {
    document.documentElement.setAttribute('data-theme', THEME_VALUE);
    localStorage.setItem('selected-theme', THEME_VALUE);
    CURRENT_THEME = THEME_VALUE;
  };

  const HANDLE_CHANGE = (EVENT: Event) => {
    APPLY_THEME((EVENT.target as HTMLSelectElement).value);
  };

  onMount(() => {
    const SAVED_THEME = localStorage.getItem('selected-theme') || 'default';
    APPLY_THEME(SAVED_THEME);
  });
</script>

<div class="theme-selector-wrapper">
  <label for="theme-selector" class="theme-selector-label">🎨</label>
  <select
    id="theme-selector"
    on:change={HANDLE_CHANGE}
    bind:value={CURRENT_THEME}
    class="theme-select"
    aria-label="Select theme"
  >
    {#each THEMES as THEME (THEME.VALUE)}
      <option value={THEME.VALUE}>{THEME.EMOJI} {THEME.LABEL}</option>
    {/each}
  </select>
</div>

<style>
  .theme-selector-wrapper {
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }

  .theme-selector-label {
    font-size: 1rem;
    cursor: default;
  }

  .theme-select {
    background: rgba(255, 255, 255, 0.15);
    color: inherit;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 0.5rem;
    padding: 0.35rem 0.6rem;
    font-size: 0.8rem;
    cursor: pointer;
    transition: background 0.2s, border-color 0.2s;
    outline: none;
  }

  .theme-select:hover,
  .theme-select:focus {
    background: rgba(255, 255, 255, 0.25);
    border-color: rgba(255, 255, 255, 0.5);
  }

  .theme-select option {
    background: #1e293b;
    color: #f1f5f9;
  }
</style>
