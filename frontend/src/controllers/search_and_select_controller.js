import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  static targets = ["searchResults", "selectedResults", "search"];
  static values = {
    searchUrl: String,
    detailUrl: String,
    type: String
  };

  connect() {
    this.selectedItems = new window.Set();
    this.loadPreselectedItems();
  }

  async loadPreselectedItems() {
    const urlParams = new URLSearchParams(window.location.search);
    const preselectedIds = urlParams.getAll(this.typeValue);

    if (preselectedIds.length > 0) {
      preselectedIds.forEach(async (id) => {
        const response = await fetch(`${this.detailUrlValue}/${id}`);
        const details = await response.json();
        this.addItemToSelection(details.id, details.name, details.post_count);
      });
    }
  }

  async search() {
    const query = this.searchTarget.value;
    if (query.length < 2) {
      this.searchResultsTarget.innerHTML = '';
      this.searchResultsTarget.classList.remove('border', 'border-zinc-200');
      return;
    }

    const response = await fetch(`${this.searchUrlValue}?query=${encodeURIComponent(query)}`);
    const items = await response.json();

    const filteredItems = items.filter(item => !this.selectedItems.has(item.id));

    if (filteredItems.length > 0) {
      this.searchResultsTarget.classList.add('border', 'border-zinc-200');
      this.searchResultsTarget.innerHTML = filteredItems.map(item => `
        <div class="cursor-pointer rounded-md p-2 text-sm text-zinc-800 hover:bg-zinc-100" data-action="click->search-and-select#addItem" data-id="${item.id}" data-name="${item.name}" data-post-count="${item.post_count || ''}">
          ${item.name}${item.post_count ? ` (${item.post_count} posts)` : ''}
        </div>
      `).join('');
    } else {
      this.searchResultsTarget.classList.remove('border', 'border-zinc-200');
      this.searchResultsTarget.innerHTML = '';
    }
  }



  addItem(event) {
    const id = event.currentTarget.dataset.id;
    const name = event.currentTarget.dataset.name;
    const postCount = event.currentTarget.dataset.postCount;
    this.addItemToSelection(id, name, postCount);

    this.searchTarget.value = '';
    this.searchResultsTarget.innerHTML = '';
  }

  addItemToSelection(id, name, postCount) {
    if (!this.selectedItems.has(id)) {
      this.selectedItems.add(id);
      this.selectedResultsTarget.insertAdjacentHTML('beforeend', `
        <div class="tag" data-id="${id}">
          ${name}${postCount ? ` (${postCount} posts)` : ''}
          <button type="button" class="ml-2 rounded-sm text-emerald-900 hover:bg-emerald-100" data-action="click->search-and-select#removeItem">
            <span class="sr-only">Remove ${name}</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18 18 6M6 6l12 12" />
            </svg>
          </button>
          <input
            type="checkbox"
            name="${this.typeValue}"
            value=${id}
            class="hidden"
            checked
          />
        </div>
      `);
    }
  }

  removeItem(event) {
    const itemElement = event.currentTarget.closest('div');
    const id = itemElement.dataset.id;
    this.selectedItems.delete(id);
    itemElement.remove();
  }
}
