  
import Franchise from './Franchise.svelte';

const franchise = new Franchise({
	target: document.getElementById("franchise-target"),
	props: JSON.parse(document.getElementById("franchise-props").textContent),
});

export default franchise;