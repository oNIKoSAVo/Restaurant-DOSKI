  
import Sign from './Sign.svelte';

const sign = new Sign({
	target: document.getElementById("sign-target"),
	props: JSON.parse(document.getElementById("sign-props").textContent),
});

export default sign;