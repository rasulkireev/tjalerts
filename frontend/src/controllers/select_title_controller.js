import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  static targets = ["item", "selected"];

  connect() {
    var startTime = performance.now();

    this.selectedTitles = {};
    this.findSelectedTitles();
    this.debouncedRender = this.debounce(this.renderSelectedTitles.bind(this), 100);
    this.debouncedRender();

    var endTime = performance.now();
    console.log(`Title 'select and render' took ${(Math.round(endTime - startTime) / 1000).toFixed(2)} seconds`);
  }

  select(event) {
    const checkbox = event.target;
    if (checkbox.matches('input[type="checkbox"]')) {
      const label = this.element.querySelector(`label[for="${checkbox.id}"]`);
      if (checkbox.checked) {
        this.selectedTitles[checkbox.id] = label.innerText.trim();
        label.classList.add('hidden');
      } else {
        delete this.selectedTitles[checkbox.id];
        label.classList.remove('hidden');
      }
      this.debouncedRender();
    }
  }

  remove(event) {
    if (event.target.matches('button[data-action="click->select-title#remove"]')) {
      const button = event.target;
      const data_id = button.dataset.id;
      const label = this.element.querySelector(`label[for="${data_id}"]`);
      const checkbox = this.element.querySelector(`input#${data_id}`);

      delete this.selectedTitles[data_id];
      label.classList.remove('hidden');
      checkbox.checked = false;

      this.debouncedRender();
    }
  }

  findSelectedTitles() {
    this.itemTargets.forEach((item) => {
      const label = this.element.querySelector(`label[for="${item.id}"]`);
      if (item.checked) {
        this.selectedTitles[item.id] = label.innerText.trim();
        label.classList.add('hidden');
      }
    });
  }

  renderSelectedTitles() {
    requestAnimationFrame(() => {
      const fragment = document.createDocumentFragment();
      Object.entries(this.selectedTitles).forEach(([id, name]) => {
        const div = document.createElement('div');
        div.className = 'flex justify-between items-center py-1';
        div.dataset.selectTitleTarget = 'selected-item';
        div.innerHTML = `
          <p>${name}</p>
          <button type="button" data-action="click->select-title#remove" data-id="${id}" class="p-1 rounded-full hover:bg-red-100">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 text-red-600">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        `;
        fragment.appendChild(div);
      });
      this.selectedTarget.innerHTML = '';
      this.selectedTarget.appendChild(fragment);
    });
  }

  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
}
