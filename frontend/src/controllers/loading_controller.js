import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
    static targets = [ "button", "loader" ];

    load() {
      this.loaderTarget.classList.replace('hidden', 'block');
      this.buttonTarget.classList.replace('bg-emerald-700', 'bg-zinc-300');
      this.buttonTarget.classList.remove('hover:bg-emerald-800');
      this.buttonTarget.disabled = true;
      document.form.submit();
    }
}
