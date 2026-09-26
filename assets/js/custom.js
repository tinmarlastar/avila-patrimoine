$(function () {

    // Header Scroll
    $(window).scroll(function () {
        if ($(window).scrollTop() >= 60) {
            $("header").addClass("fixed-header");
        } else {
            $("header").removeClass("fixed-header");
        }
    });


    // Featured Owl Carousel
    var $featured = $('.featured-projects-slider .owl-carousel');
    $featured.owlCarousel({
        center: false, // cartes entières, alignées à gauche (plus de carte coupée)
        loop: true,
        margin: 30,
        nav: false,
        dots: false,
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: false,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 3
            },
            1200: {
                items: 4
            }
        }
    })

    // Glissement latéral au pavé tactile (ou molette horizontale) : une carte par geste
    var cumul = 0, bloque = false;
    $featured.each(function () {
        this.addEventListener('wheel', function (e) {
            if (Math.abs(e.deltaX) <= Math.abs(e.deltaY)) return; // défilement vertical : on laisse la page défiler
            e.preventDefault(); // évite le « retour arrière » du navigateur
            if (bloque) return;
            cumul += e.deltaX;
            if (Math.abs(cumul) < 30) return;
            $featured.trigger(cumul > 0 ? 'next.owl.carousel' : 'prev.owl.carousel', [600]);
            cumul = 0; bloque = true;
            setTimeout(function () { bloque = false; }, 650);
        }, { passive: false });
    });


    // Count
    $('.count').each(function () {
		$(this).prop('Counter', 0).animate({
			Counter: $(this).text()
		}, {
			duration: 1000,
			easing: 'swing',
			step: function (now) {
				$(this).text(Math.ceil(now));
			}
		});
	});


    // ScrollToTop
    function scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }

    const btn = document.getElementById("scrollToTopBtn");
    btn.addEventListener("click", scrollToTop);

    window.onscroll = function () {
        const btn = document.getElementById("scrollToTopBtn");
        if (document.documentElement.scrollTop > 100 || document.body.scrollTop > 100) {
            btn.style.display = "flex";
        } else {
            btn.style.display = "none";
        }
    };


    // Aos
	AOS.init({
		once: true,
	});

});

