/* Template: Sync - Free Mobile App Landing Page HTML Template
   Author: Inovatik
   Created: Dec 2019
   Description: Custom JS file
*/


(function($) {
    "use strict"; 
	
	/* Preloader */
	$(window).on('load', function() {
		var preloaderFadeOutTime = 500;
		function hidePreloader() {
			var preloader = $('.spinner-wrapper');
			setTimeout(function() {
				preloader.fadeOut(preloaderFadeOutTime);
			}, 900);
		}
		hidePreloader();
	});

	
	/* Navbar Scripts */
	// jQuery to collapse the navbar on scroll
    $(window).on('scroll load', function() {
		if ($(".navbar").offset().top > 60) {
			$(".fixed-top").addClass("top-nav-collapse");
		} else {
			$(".fixed-top").removeClass("top-nav-collapse");
		}
    });

	// jQuery for page scrolling feature - requires jQuery Easing plugin
	$(function() {
		$(document).on('click', 'a.page-scroll', function(event) {
			var $anchor = $(this);
			$('html, body').stop().animate({
				scrollTop: $($anchor.attr('href')).offset().top
			}, 600, 'easeInOutExpo');
			event.preventDefault();
		});
	});

    // closes the responsive menu on menu item click
    $(".navbar-nav li a").on("click", function(event) {
    if (!$(this).parent().hasClass('dropdown'))
        $(".navbar-collapse").collapse('hide');
    });


    // /* Image Slider - Swiper */
    // var imageSlider = new Swiper('.image-slider', {
    //     autoplay: {
    //         delay: 2000,
    //         disableOnInteraction: false
	// 	},
    //     loop: false,
    //     navigation: {
	// 		nextEl: '.swiper-button-next',
	// 		prevEl: '.swiper-button-prev',
	// 	},
    //     spaceBetween: 30,
    //     slidesPerView: 5,
	// 	breakpoints: {
    //         // when window is <= 516px
    //         516: {
    //             slidesPerView: 1,
    //             spaceBetween: 10
    //         },
    //         // when window is <= 767px
    //         767: {
    //             slidesPerView: 2,
    //             spaceBetween: 20
    //         },
    //         // when window is <= 991px
    //         991: {
    //             slidesPerView: 3,
    //             spaceBetween: 30
    //         },
    //         // when window is <= 1199px
    //         1199: {
    //             slidesPerView: 4,
    //             spaceBetween: 30
    //         },
    //     }
    // });


    

})(jQuery);