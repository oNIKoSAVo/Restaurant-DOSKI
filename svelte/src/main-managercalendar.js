import ManagerCalendar from './ManagerCalendar.svelte';

const managerCalendar = new ManagerCalendar({
	target: document.getElementById("managercalendar-target"),
	props: JSON.parse(document.getElementById("managercalendar-props").textContent),
});

export default managerCalendar;
