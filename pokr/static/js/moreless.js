$(document).ready(function () {
$('.read-more-content').addClass('sometimes-hide')
$('.read-more-show, .read-more-hide').removeClass('sometimes-hide')

$('.read-more-show').on('click', function(e) {
  $(this).next('.read-more-content').removeClass('sometimes-hide');
  $(this).addClass('sometimes-hide');
  e.preventDefault();
});

$('.read-more-hide').on('click', function(e) {
  var p = $(this).parent('.read-more-content');
  p.addClass('sometimes-hide');
  p.prev('.read-more-show').removeClass('sometimes-hide');
  e.preventDefault();
});
});
