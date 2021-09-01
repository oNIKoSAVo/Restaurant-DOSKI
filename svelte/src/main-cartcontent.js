import CartContent from "./CartContent.svelte";

const cartContent = new CartContent({
  target: document.getElementById("cartcontent-target"),
  props: JSON.parse(document.getElementById("cartсontent-props").textContent),
  // props: JSON.parse(document.getElementById("cartcontent-props").textContent),
});

export default cartContent;
