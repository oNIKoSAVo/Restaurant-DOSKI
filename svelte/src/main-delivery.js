  
import Delivery from './Delivery.svelte';

const delivery = new Delivery({
	target: document.getElementById("delivery-target"),
	props: JSON.parse(document.getElementById("delivery-props").textContent),
});

export default delivery;