<script>
  export let imgSrc;
  export let quantity;
  export let price;
</script>

<div class="cart-item">
  <div class="cart-item_imgwrapper">
    <img class="cart-item_img" src={imgSrc} />
  </div>
  <div class="cart-item_title">Пицца «Ди Поло» 375гр</div>
  <div class="calculation-wrap">
    <div class="calculations">
      <div class="minus-btn">-</div>
      <div class="item-quantity">{quantity}</div>
      <div class="plus-btn">+</div>
    </div>
  </div>
  <div class="cart-item_price text-right">{price}.-</div>
</div>
