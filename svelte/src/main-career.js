  
import Career from './Career.svelte';

const career = new Career({
	target: document.getElementById("career-target"),
	props: JSON.parse(document.getElementById("career-props").textContent),
});

export default career;