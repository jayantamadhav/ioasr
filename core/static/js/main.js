function sanitizeString(str) {
  str = str.replace(/[^a-z0-9áéíóúñü \.,_-]/gim, "");
  return str.trim().toLowerCase().replace(/ /g, "+");
}

const screens = {
  sm: window.matchMedia("(max-width: 640px)"),
  md: window.matchMedia("(max-width: 768px)"),
  lg: window.matchMedia("(max-width: 1024px)"),
  xl: window.matchMedia("(max-width: 1280px)"),
  "2xl": window.matchMedia("(max-width: 1536px)"),
};

function sanitizeString(str) {
  str = str.replace(/[^a-z0-9áéíóúñü \.,_-]/gim, "");
  return str.trim().toLowerCase().replace(/ /g, "+");
}

$(document).ready(function () {

  $(".author-link").on("click", function () {
    const authorId = $(this).data("author-id");
    const journalUrl = $(this).data("journal-url");
    window.location.href = `${window.location.origin}/${journalUrl}/publications?author=${authorId}`;
  });

  $("#publisher-search-btn").on("click", function (e) {
    e.preventDefault();
    let keywords = $("#ps_keywords").val();
    let author = $("#ps_author").val();
    let journal = $("#ps_journal").val();
    let articleType = $("#ps_articleType").val();

    let url = $("#publisher-search").data("action");
    console.log(url);
    url = `${url}?journal=${journal}&articleType=${articleType}`;
    if (keywords) {
      url = `${url}&keywords=${keywords}`;
    }
    if (author) {
      url = `${url}&author=${author}`;
    }
    console.log(url);

    window.location.href = url;
  });

  $("#ohc-journal").on("change", async function (e) {
    const res = await fetch(`${window.location.href}?journal=${$(this).val()}`);
    if (!res.ok) {
      throw new Error(`HTTP error! Status: ${res.status}`);
    }
    const data = JSON.parse(await res.json());

    // Update volumes
    if (data.length > 0) {
      $("#ohc-volumes").empty();
      $("#ohc-volumes").append(
        "<option selected disabled>Choose Volume</option>"
      );
      for (var i = 0; i < data.length; i++) {
        $("#ohc-volumes").append(
          `<option value="${data[i].pk}">${data[i].fields.name} (${data[i].fields.year})</option>`
        );
      }
    }
  });

  $("#ohc-volumes").on("change", async function () {
    const res = await fetch(`${window.location.href}?volume=${$(this).val()}`);
    if (!res.ok) {
      throw new Error(`HTTP error! Status: ${res.status}`);
    }
    const data = JSON.parse(await res.json());
    // Update issues
    if (data.length > 0) {
      $("#ohc-issues").empty();
      $("#ohc-issues").append(
        "<option selected disabled>Choose Issue</option>"
      );
      for (var i = 0; i < data.length; i++) {
        $("#ohc-issues").append(
          `<option value="${data[i].pk}">${data[i].fields.name} (${data[i].fields.month})</option>`
        );
      }
    }
  });

  $("#payment-form").on("submit", function (e) {
    e.preventDefault();
    $("#payment-form").addClass("hidden");
    $("#payment-loader").removeClass("hidden");

    const data = {
      csrfToken: $("#payment_csrf_token").val(),
      name: $("#payment_name").val(),
      email: $("#payment_email").val(),
      phone: $("#payment_phone").val(),
      country: $("#payment_country").val(),
      amount: $("#payment_amount").val(),
      currency: $("#payment_currency").val(),
    };
    console.log(data);
    fetch("", {
      method: "POST",
      cache: "no-cache",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": data.csrfToken,
      },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        data = JSON.parse(data);
        const origin = location.protocol + "//" + location.host;
        let options = {
          key: data.RAZORPAY_API_KEY,
          amount: data.amount,
          currency: data.currency,
          name: "iARCON International LLP",
          description: "Payment",
          image: "https://hub.iarcon.org/assets/logo-fa996dec.jpeg",
          order_id: data.order_id,
          callback_url: `${origin}/payments/callback/`,
          prefill: {
            name: data.name,
            email: data.email,
            contact: data.phone,
          },
        };
        console.log(options);
        var rzp = new Razorpay(options);
        rzp.open();
        rzp.on("payment.success", function (e) {
          console.log("success", e);
        });
      })
      .catch((error) => {
        console.error("There was a problem with your fetch operation:", error);
      });
  });

  $("#submitResearch").on("submit", function (e) {
    const link = $("#submitResearchJournal").val();
    // window.location.href = link;
    window.open(link, "_blank");
  });



  const downloadPDFModal = $("#download-pdf-modal");
  const downloadPDFModalOpen = $(".download-pdf-modal-open");
  const downloadPDFModalClose = $(".download-pdf-modal-close");

  downloadPDFModalOpen.on("click", function () {
    const articleId = $(this).data("article-id");
    $("#download-pdf-modal-articleid").val(articleId);
    
    $('html').css('overflow', 'hidden');
    downloadPDFModal.removeClass("hidden");
  });
  downloadPDFModalClose.on("click", function () {

    $('html').css('overflow', 'auto');
    downloadPDFModal.addClass("hidden");
  });
  $(document).on("click", function (event) {
    if (
      !downloadPDFModal.hasClass("hidden") &&
      !$(event.target).closest(".modal-content").length &&
      !$(event.target).is(downloadPDFModalOpen)
    ) {
      downloadPDFModal.removeClass('overflow-hidden');
      $('html').css('overflow', 'auto');
      downloadPDFModal.addClass("hidden");
    }
  });
});
