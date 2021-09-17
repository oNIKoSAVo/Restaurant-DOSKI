function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export const getCSRFtoken = function() {
    return getCookie("csrftoken")
}


export const ModalHiddenEventListener = (el, fn, owner) => {
  const opts = {
      attributeFilter: ['style']
  },
  mo = new MutationObserver(mutations => {
      for (let mutation of mutations) {
          if (mutation.type === 'attributes' 
          && mutation.attributeName ==='style' ) {
              mo.disconnect();
              fn({
                  owner: owner,
                  element: mutation.target
              });
          }
      }
  });
  mo.observe(el, opts);
};