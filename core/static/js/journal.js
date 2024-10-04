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
$(document).ready(function () {
  try {
    $(".indexingSlick").slick({
      dots: false,
      arrows: false,
      infinite: true,
      autoplay: true,
      autoplaySpeed: 4000,
      slidesToShow: 1,
      slidesToScroll: 1,
    });
  } catch (err) {
    console.log("slick not initialized");
  }

  $("#navbarSearch").on("keypress", function (e) {
    if (e.which == 13) {
      window.location.href = `${window.location.origin}/${
        window.location.pathname.split("/")[1]
      }/search?q=${$(this).val()}`;
    }
  });

  const sidebar = document.getElementById("navSidebar");
  const toggleSidebarBtn = document.getElementById("toggleNavSidebar");

  // Function to open the sidebar
  function openSidebar() {
    sidebar.classList.remove("-translate-x-full");
  }

  // Function to close the sidebar
  function closeSidebar() {
    sidebar.classList.add("-translate-x-full");
  }

  // Toggle the sidebar when the button is clicked
  toggleSidebarBtn.addEventListener("click", function () {
    if (sidebar.classList.contains("-translate-x-full")) {
      openSidebar();
    } else {
      closeSidebar();
    }
  });

  document.addEventListener("click", function (event) {
    if (
      !sidebar.contains(event.target) &&
      !toggleSidebarBtn.contains(event.target)
    ) {
      closeSidebar();
    }
  });

  $(".article-abstract-btn").on("click", function () {
    const articleId = $(this).data("article");
    const abstractBlock = $(`#article-abstract-block-${articleId}`);
    abstractBlock.toggleClass("hidden");
  });

  const navbarContainer = document.getElementById("navbarContainer");
  const navbar2 = document.getElementById("navbar2");
  const navbar2Logo = document.getElementById("navbar2Logo");
  const navbar2Brand = document.getElementById("navbar2Brand");
  const navbar3 = document.getElementById("navbar3");
  const navbarJournalName = document.getElementById("navbarJournalName");
  let isNavbarShrunk = false;

  function debounce(func, delay) {
    let timer;
    return function () {
      clearTimeout(timer);
      timer = setTimeout(() => {
        func.apply(this, arguments);
      }, delay);
    };
  }

  const toggleNavbarShrink = debounce(() => {
    // if (
    //   window.scrollY > 200 &&
    //   !navbar1.classList.contains("hidden")
    // ) {
    //   navbar1.classList.add("hidden");
    // } else if ( window.scrollY < 90 && navbar1.classList.contains("hidden")) {
    //   navbar1.classList.remove("hidden");
    // }

    if (!screens.sm.matches) {
      if (window.scrollY > 180) {
        navbar2Logo.classList.add("hidden");
      } else if (window.scrollY < 90) {
        navbar2Logo.classList.remove("hidden");
      }
    }

    if (window.scrollY > 180 && !isNavbarShrunk) {
      navbar2.classList.remove("lg:py-12");
      navbar2Brand.classList.remove("lg:ml-10");
      navbar2.classList.remove("lg:py-12");
      navbarJournalName.classList.remove("text-3xl");
      navbarJournalName.classList.remove("lg:text-4xl");
      navbarJournalName.classList.add("lg:text-2xl");
      isNavbarShrunk = true;
    } else if (window.scrollY < 90 && isNavbarShrunk) {
      navbar2.classList.add("lg:py-12");
      navbar2Brand.classList.add("lg:ml-10");
      navbarJournalName.classList.add("text-3xl");
      navbarJournalName.classList.add("lg:text-4xl");
      navbarJournalName.classList.remove("lg:text-2xl");
      navbar2.classList.add("lg:py-12");
      isNavbarShrunk = false;
    }
  });

  toggleNavbarShrink();

  window.addEventListener("scroll", toggleNavbarShrink);

  $(".author-link").on("click", function () {
    const authorId = $(this).data("author-id");
    const journalUrl = $(this).data("journal-url");
    window.location.href = `${window.location.origin}/${journalUrl}/publications?author=${authorId}`;
  });

  $("#currency").on("change", function () {
    const paytmBtn = $("#payWithPaytmBtn");
    const stripeBtn = $("#payWithStripeBtn");
    if ($(this).val() === "inr") {
      paytmBtn.removeClass("hidden");
      paytmBtn.addClass("inline-flex");
      stripeBtn.addClass("hidden");
      stripeBtn.removeClass("inline-flex");
    } else {
      paytmBtn.removeClass("inline-flex");
      paytmBtn.addClass("hidden");
      stripeBtn.removeClass("hidden");
      stripeBtn.addClass("inline-flex");
    }
  });

  function openModal(modalId) {
    const modal = $(`#${modalId}`);
    modal.css("display", "flex");
    modal.css("justify-content", "center");
    modal.css("align-items", "center");
    $("html, body").addClass("overflow-hidden");
  }

  // Function to close the modal
  function closeModal(modalId) {
    const modal = $(`#${modalId}`);
    modal.css("display", "none");
    $("html, body").removeClass("overflow-hidden");
  }

  // Event listener for opening the modal
  $(".openModal").on("click", function () {
    const modalId = $(this).data("modal-id");
    openModal(modalId);
  });

  // Event listener for closing the modal
  $(".closeModal").on("click", function () {
    const modalId = $(this).data("modal-id");
    closeModal(modalId);
  });

  $(".keyword-search").on("click", function () {
    function replaceNonAlphabets(input) {
      // Regular expression to match non-alphabetic characters
      var regex = /[^a-zA-Z]+/g;

      // Replace non-alphabetic characters with '+'
      var result = input.toLowerCase().replace(regex, "+");

      // Remove trailing '+' if any
      if (result.endsWith("+")) {
        result = result.slice(0, -1);
      }

      return result;
    }
    let word = $(this).data("word");
    console.log(word);
    word = replaceNonAlphabets(word);
    window.location.href = `${window.location.origin}/search?journal=All&articleType=All&keywords=${word}`;
  });

  // For download-pdf-modal
  const downloadPDFModal = $("#download-pdf-modal");
  const downloadPDFModalOpen = $(".download-pdf-modal-open");
  const downloadPDFModalClose = $(".download-pdf-modal-close");

  downloadPDFModalOpen.on("click", function () {
    const articleId = $(this).data("article-id");
    $("#download-pdf-modal-articleid").val(articleId);

    $("html").css("overflow", "hidden");
    downloadPDFModal.removeClass("hidden");
  });
  downloadPDFModalClose.on("click", function () {
    $("html").css("overflow", "auto");
    downloadPDFModal.addClass("hidden");
  });
  $(document).on("click", function (event) {
    if (
      !downloadPDFModal.hasClass("hidden") &&
      !$(event.target).closest(".modal-content").length &&
      !$(event.target).is(downloadPDFModalOpen)
    ) {
      downloadPDFModal.removeClass("overflow-hidden");
      $("html").css("overflow", "auto");
      downloadPDFModal.addClass("hidden");
    }
  });

  // For smooth scrolling when anchor clicked
  $(document).on("click", 'a[href^="#"]', function (event) {
    event.preventDefault();

    $("html, body").animate(
      {
        scrollTop: $($.attr(this, "href")).offset().top,
      },
      500
    );
  });
});
