<script lang="ts">
	import { toast } from 'svelte-sonner';
	import dayjs from 'dayjs';
	import { getContext, createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	import Modal from '$lib/components/common/Modal.svelte';
	import { getUsageListByUserId } from '$lib/apis/usages';
	import Tooltip from '$lib/components/common/Tooltip.svelte';

	const i18n = getContext('i18n');

	export let show = false;
	export let user;

	let usages = [];

	$: if (show) {
		(async () => {
			if (user.id) {
				let page = 0;
				usages = await getUsageListByUserId(localStorage.token, page, user.id);
			}
		})();
	}
	let sortKey = 'created_at'; // default sort key
	let sortOrder = 'desc'; // default sort order
	function setSortKey(key) {
		if (sortKey === key) {
			sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
		} else {
			sortKey = key;
			sortOrder = 'asc';
		}
	}
</script>

<Modal size="lg" bind:show>
	<div>
		<div class=" flex justify-between dark:text-gray-300 px-5 py-4">
			<div class=" text-lg font-medium self-center capitalize">
				{$i18n.t("{{user}}'s Usages", { user: user.name })}
			</div>
			<button
				class="self-center"
				on:click={() => {
					show = false;
				}}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
					class="w-5 h-5"
				>
					<path
						d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
					/>
				</svg>
			</button>
		</div>
		<hr class=" dark:border-gray-850" />

		<div class="flex flex-col md:flex-row w-full px-5 py-4 md:space-x-4 dark:text-gray-200">
			<div class=" flex flex-col w-full sm:flex-row sm:justify-center sm:space-x-6">
				{#if usages.length > 0}
					<div class="text-left text-sm w-full mb-4 max-h-[22rem] overflow-y-scroll">
						<div class="relative overflow-x-auto">
							<table class="w-full text-sm text-left text-gray-600 dark:text-gray-400 table-auto">
								<thead
									class="text-xs text-gray-700 uppercase bg-transparent dark:text-gray-200 border-b-2 dark:border-gray-800"
								>
									<tr>
										<th
											scope="col"
											class="px-3 py-2 cursor-pointer select-none"
											on:click={() => setSortKey('model')}
										>
											{$i18n.t('Model')}
											{#if sortKey === 'model'}
												{sortOrder === 'asc' ? '▲' : '▼'}
											{:else}
												<span class="invisible">▲</span>
											{/if}
										</th>
										<th
											scope="col"
											class="px-3 py-2 cursor-pointer select-none"
											on:click={() => setSortKey('model')}
										>
											{$i18n.t('Token Count')}
											{#if sortKey === 'token_count'}
												{sortOrder === 'asc' ? '▲' : '▼'}
											{:else}
												<span class="invisible">▲</span>
											{/if}
										</th>
										<th
											scope="col"
											class="px-3 py-2 hidden md:flex cursor-pointer select-none"
											on:click={() => setSortKey('created_at')}
										>
											{$i18n.t('Updated at')}
											{#if sortKey === 'created_at'}
												{sortOrder === 'asc' ? '▲' : '▼'}
											{:else}
												<span class="invisible">▲</span>
											{/if}
										</th>
										<th scope="col" class="px-3 py-2 text-right" />
									</tr>
								</thead>
								<tbody>
									{#each usages.sort((a, b) => {
										if (a[sortKey] < b[sortKey]) return sortOrder === 'asc' ? -1 : 1;
										if (a[sortKey] > b[sortKey]) return sortOrder === 'asc' ? 1 : -1;
										return 0;
									}) as usage, idx}
										<tr
											class="bg-transparent {idx !== usages.length - 1 &&
												'border-b'} dark:bg-gray-900 dark:border-gray-850 text-xs"
										>
											<td class="px-3 py-1">
												<div class="line-clamp-1">
													{usage.model}
												</div>
											</td>

											<td class="px-3 py-1">
												<div class="line-clamp-1">
													{usage.token_count}
												</div>
											</td>
											<td class=" px-3 py-1 hidden md:flex h-[2.5rem]">
												<div class="my-auto">
													{dayjs(usage.created_at * 1000).format($i18n.t('MMMM DD, YYYY HH:mm:ss'))}
												</div>
											</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					</div>
				{:else}
					<div class="text-left text-sm w-full mb-8">
						{user.name}
						{$i18n.t('has no usages.')}
					</div>
				{/if}
			</div>
		</div>
	</div>
</Modal>
