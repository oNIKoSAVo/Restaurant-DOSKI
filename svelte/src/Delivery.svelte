<script>
  let price = 0;
  let cart = [];

  // $: document.querySelector(".cart-summary").textContent = price;

  function getPrice(parentNode) {
    return Number(
      parentNode.parentNode
        .querySelector(".dish-details_price")
        .textContent.slice(0, -2)
        .replace(",", ".")
    );
  }

  function setPrice() {
    document.querySelector(".cart-summary").textContent = price + ".-";
  }

  document
    .querySelectorAll(".minus-btn")
    .forEach((elem) =>
      elem.addEventListener("click", (e) => handleClickOnMinus(e))
    );
  document
    .querySelectorAll(".plus-btn")
    .forEach((elem) =>
      elem.addEventListener("click", (e) => handleClickOnPlus(e))
    );

  function handleClickOnMinus(e) {
    const parentNode = e.target.parentNode;

    const menueId = parentNode.getAttribute("data-menue-id");
    // console.log(menueId);
    const quantity = parentNode.querySelector(".item-quantity").innerText;

    if (parseInt(quantity) === 0) return;
    parentNode.querySelector(".item-quantity").innerText =
      parseInt(quantity) - 1;
    const menuItemPrice = getPrice(parentNode);
    price -= menuItemPrice;
    setPrice();
  }

  function handleClickOnPlus(e) {
    const parentNode = e.target.parentNode;
    const productCard = e.target.parentNode.parentNode.parentNode;
    console.log({ productCard });
    const menuItemPrice = getPrice(parentNode);
    const productIndex = cart.findIndex((el) => {
      return el.name === productCard.querySelector(".dish-title").textContent;
    });
    // console.log({ productCard });
    if (productIndex !== -1) {
      cart = cart.map((el, i) => {
        if (i === productIndex) el.quantity++;
        return el;
      });
    } else {
      cart = [
        ...cart,
        {
          price: menuItemPrice,
          name: productCard.querySelector(".dish-title").textContent,
          quantity: 1,
          img: productCard.querySelector(".dish-img").getAttribute("src"),
        },
      ];
    }
    console.log({ cart });
    price += menuItemPrice;
    const menueId = parentNode.getAttribute("data-menue-id");
    // console.log(menueId);
    let quantity = parentNode.querySelector(".item-quantity").innerText;
    setPrice();
    parentNode.querySelector(".item-quantity").innerText =
      parseInt(quantity) + 1;
  }
</script>
