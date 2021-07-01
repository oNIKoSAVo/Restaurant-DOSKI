  
import Feedback from './Feedback.svelte';

const feedback = new Feedback({
	target: document.getElementById("feedback-target"),
	props: JSON.parse(document.getElementById("feedback-props").textContent),
});

export default feedback;