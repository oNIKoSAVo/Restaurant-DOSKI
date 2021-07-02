  
import Reservation from './Reservation.svelte';

const reservation = new Reservation({
	target: document.getElementById("reservation-target"),
	props: JSON.parse(document.getElementById("reservation-props").textContent),
});

export default reservation;