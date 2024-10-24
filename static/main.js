fetch("/donation/config/")
  .then((result) => {
    return result.json();
  })
  .then((data) => {
    const stripe = Stripe(data.publicKey);
    const buttons = document.querySelectorAll(".donation-btn");
    buttons.forEach((button) => {
      const id = button.getAttribute("data-id");
      button.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        fetch("/donation/create-checkout-session/" + id)
          .then((result) => {
            return result.json();
          })
          .then((data) => {
            console.log(data);
            return stripe.redirectToCheckout({ sessionId: data.sessionId });
          })
          .then((res) => {
            console.log(res);
          });
      });
    });
    console.log("Stripe Ready");
  });
