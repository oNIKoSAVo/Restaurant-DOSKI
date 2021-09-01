<script>
  document.querySelectorAll('.minus-btn').forEach(elem => elem.addEventListener("click", (e) => handleClickOnMinus(e)))
  document.querySelectorAll('.plus-btn').forEach(elem => elem.addEventListener("click", (e) => handleClickOnPlus(e)))

  function handleClickOnMinus(e){
    let parentNode = e.target.parentNode;
    let menueId = parentNode.getAttribute('data-menue-id');
    console.log(menueId);
    let quantity = parentNode.querySelector('.item-quantity').innerText;
    parentNode.querySelector('.item-quantity').innerText = parseInt(quantity) - 1;

  }

  function handleClickOnPlus(e){
    let parentNode = e.target.parentNode;
    let menueId = parentNode.getAttribute('data-menue-id');
    console.log(menueId);
    let quantity = parentNode.querySelector('.item-quantity').innerText;
    parentNode.querySelector('.item-quantity').innerText = parseInt(quantity) + 1;
  }
</script>