<script lang="ts">
    import { onMount } from "svelte";

    interface Dog {
        id: number;
        name: string;
        breed: string;
        status: string;
        image_url: string | null;
    }

    interface Breed {
        id: number;
        name: string;
    }

    export let DOGS: Dog[] = [];
    let BREEDS: Breed[] = [];
    let SELECTED_BREED_ID = "";
    let SHOW_AVAILABLE_ONLY = false;
    let LOADING = true;
    let ERROR: string | null = null;

    const FETCH_BREEDS = async () => {
        try {
            const RESPONSE = await fetch('/api/breeds');
            if (RESPONSE.ok) {
                BREEDS = await RESPONSE.json();
            }
        } catch (ERR) {
            console.error('Failed to fetch breeds:', ERR);
        }
    };

    const FETCH_DOGS = async () => {
        LOADING = true;
        try {
            const PARAMS = new URLSearchParams();
            if (SELECTED_BREED_ID) {
                PARAMS.set('breed_id', SELECTED_BREED_ID);
            }
            if (SHOW_AVAILABLE_ONLY) {
                PARAMS.set('available', 'true');
            }
            const QUERY_STRING = PARAMS.toString();
            const URL = `/api/dogs${QUERY_STRING ? `?${QUERY_STRING}` : ''}`;
            const RESPONSE = await fetch(URL);
            if(RESPONSE.ok) {
                DOGS = await RESPONSE.json();
            } else {
                ERROR = `Failed to fetch data: ${RESPONSE.status} ${RESPONSE.statusText}`;
            }
        } catch (ERR) {
            ERROR = `Error: ${ERR instanceof Error ? ERR.message : String(ERR)}`;
        } finally {
            LOADING = false;
        }
    };

    const HANDLE_BREED_CHANGE = (EVENT: Event) => {
        SELECTED_BREED_ID = (EVENT.target as HTMLSelectElement).value;
        FETCH_DOGS();
    };

    const HANDLE_AVAILABLE_CHANGE = (EVENT: Event) => {
        SHOW_AVAILABLE_ONLY = (EVENT.target as HTMLInputElement).checked;
        FETCH_DOGS();
    };

    onMount(() => {
        FETCH_BREEDS();
        FETCH_DOGS();
    });
</script>

<div>
    <h2 class="text-2xl font-medium mb-6 text-slate-100">Available Dogs</h2>

    <!-- Filter Controls -->
    <div class="flex flex-wrap gap-4 mb-6 items-center">
        <div class="flex items-center gap-2">
            <label for="breed-filter" class="text-slate-300 text-sm font-medium">Breed:</label>
            <select
                id="breed-filter"
                on:change={HANDLE_BREED_CHANGE}
                class="bg-slate-800 text-slate-200 border border-slate-600 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
            >
                <option value="">All Breeds</option>
                {#each BREEDS as BREED (BREED.id)}
                    <option value={BREED.id}>{BREED.name}</option>
                {/each}
            </select>
        </div>
        <div class="flex items-center gap-2">
            <input
                id="available-filter"
                type="checkbox"
                on:change={HANDLE_AVAILABLE_CHANGE}
                class="w-4 h-4 rounded border-slate-600 bg-slate-800 text-blue-500 focus:ring-blue-500 focus:ring-offset-0"
            />
            <label for="available-filter" class="text-slate-300 text-sm font-medium">Available only</label>
        </div>
    </div>
    
    {#if LOADING}
        <!-- loading animation -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each Array(6) as _, i}
                <div class="bg-slate-800/60 backdrop-blur-sm rounded-xl overflow-hidden shadow-lg border border-slate-700/50">
                    <div class="p-6">
                        <div class="animate-pulse">
                            <div class="h-6 bg-slate-700 rounded w-3/4 mb-3"></div>
                            <div class="h-4 bg-slate-700 rounded w-1/2 mb-4"></div>
                            <div class="h-4 bg-slate-700 rounded w-1/4 mt-6"></div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {:else if ERROR}
        <!-- error display -->
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <p class="text-red-400">{ERROR}</p>
        </div>
    {:else if DOGS.length === 0}
        <!-- no dogs found -->
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <p class="text-slate-300">No dogs available at the moment.</p>
        </div>
    {:else}
        <!-- dog list -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each DOGS as DOG (DOG.id)}
                <a 
                    href={`/dog/${DOG.id}`} 
                    class="group block bg-slate-800/60 backdrop-blur-sm rounded-xl overflow-hidden shadow-lg border border-slate-700/50 hover:border-blue-500/50 hover:shadow-blue-500/10 hover:shadow-xl transition-all duration-300 hover:translate-y-[-6px]"
                >
                    <img
                        src={DOG.image_url || 'https://placedog.net/400/300'}
                        alt={DOG.name}
                        class="w-full h-48 object-cover"
                        on:error={(E) => { (E.currentTarget as HTMLImageElement).src = 'https://placedog.net/400/300'; }}
                    />
                    <div class="p-6 relative">
                        <div class="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                        <div class="relative z-10">
                            <h3 class="text-xl font-semibold text-slate-100 mb-2 group-hover:text-blue-400 transition-colors">{DOG.name}</h3>
                            <p class="text-slate-400 mb-1">{DOG.breed}</p>
                            <span class="inline-block text-xs font-medium px-2 py-0.5 rounded-full {DOG.status === 'AVAILABLE' ? 'bg-green-500/20 text-green-400' : DOG.status === 'PENDING' ? 'bg-yellow-500/20 text-yellow-400' : 'bg-slate-500/20 text-slate-400'}">
                                {DOG.status === 'AVAILABLE' ? 'Available' : DOG.status === 'PENDING' ? 'Pending' : 'Adopted'}
                            </span>
                            <div class="mt-4 text-sm text-blue-400 font-medium flex items-center">
                                <span>View details</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1 transform transition-transform duration-300 group-hover:translate-x-2" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </a>
            {/each}
        </div>
    {/if}
</div>