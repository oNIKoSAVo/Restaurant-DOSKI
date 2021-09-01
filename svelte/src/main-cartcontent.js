import CartContent from "./CartContent.svelte";

const cartContent = new CartContent({
  target: document.getElementById("cartcontent-target"),
  props: {
    cartContent: JSON.parse(
      document.getElementById("cartcontent-props").textContent
    ),
  },
  // props: JSON.parse(document.getElementById("cartcontent-props").textContent),
});

export default cartContent;
