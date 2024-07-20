import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  static targets = ["results", "selected"];

  connect() {
    this.selectedTechnologies = {};
    this.debouncedSearch = this.debounce(this.performSearch.bind(this), 300);
  }

  search(event) {
    const query = event.target.value.trim();
    if (query.length >= 2) {
      this.debouncedSearch(query);
    } else {
      this.resultsTarget.innerHTML = '';
    }
  }

  async performSearch(query) {
    try {
      const response = await fetch(`/api/technologies/search?query=${encodeURIComponent(query)}`);
      if (!response.ok) throw new Error('Network response was not ok');
      const technologies = await response.json();
      this.renderResults(technologies);
    } catch (error) {
      console.error('Error fetching technologies:', error);
    }
  }

  renderResults(technologies) {
    const fragment = document.createDocumentFragment();
    technologies.forEach(tech => {
      const div = document.createElement('div');
      div.className = 'flex items-center py-1';
      div.dataset.selectTechnologyTarget = 'selected';
      div.innerHTML = `
        <input type="checkbox" id="${tech.id}" value="${tech.id}" class="mr-2" data-action="change->select-technology#select">
        <label for="${tech.id}">${tech.name} (${tech.post_count})</label>
      `;
      fragment.appendChild(div);
    });
    this.resultsTarget.innerHTML = '';
    this.resultsTarget.appendChild(fragment);
  }

  select(event) {
    const checkbox = event.target;
    const label = checkbox.nextElementSibling;
    if (checkbox.checked) {
      this.selectedTechnologies[checkbox.id] = label.innerText.trim();
    } else {
      delete this.selectedTechnologies[checkbox.id];
    }
    this.renderSelectedTechnologies();
  }

  remove(event) {
    if (event.target.matches('button[data-action="click->select-technology#remove"]')) {
      const button = event.target;
      const data_id = button.dataset.id;
      const checkbox = this.resultsTarget.querySelector(`input#${data_id}`);

      delete this.selectedTechnologies[data_id];
      if (checkbox) checkbox.checked = false;

      this.renderSelectedTechnologies();
    }
  }

  renderSelectedTechnologies() {
    const fragment = document.createDocumentFragment();
    Object.entries(this.selectedTechnologies).forEach(([id, name]) => {
      const div = document.createElement('div');
      div.className = 'flex justify-between items-center py-1';
      div.dataset.selectTechnologyTarget = 'selected-item';
      div.innerHTML = `
        <p>${name}</p>
        <button type="button" data-action="click->select-technology#remove" data-id="${id}" class="p-1 rounded-full hover:bg-red-100">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4 text-red-600">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      `;
      fragment.appendChild(div);
    });
    this.selectedTarget.innerHTML = '';
    this.selectedTarget.appendChild(fragment);
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
