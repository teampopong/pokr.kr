(function () {

var namespace = 'cards-cart',
    items = [],
    $cart = $('#'+namespace);

// TODO: Load the template from the server dynamically
var TMPL_CARD = '\
<div class="card card-small">\
    <a class="person-link" href="{{url}}">\
        <img class="person-img" src="{{image}}">\
        <div class="person-name">{{name}}</div>\
    </a>\
    <a class="btn-remove-card" href="#" onclick="CART.removeCard(this); return false;">x</a>\
</div>\
';

window.CART = {};
    
$(function () {
    loadCards();
});

function clearCards() {
    $cart.empty();
}

function loadCards() {
    clearCards();

    items = localStorage.getItem(namespace) || '[]';

    try {
        items = JSON.parse(items);
    } catch (e) {
        if (console && console.error) {
            console.error('error loading cart items');
        }
    }

    $.each(items, function (i, item) {
        prependCard(item);
    });
}

function prependCard(item) {
    var $item = $(item).appendTo($cart);
    $item.find('.person-img').clipImage();
}

function saveCards() {
    localStorage.setItem(namespace, JSON.stringify(items));
}

CART.clearCart = function () {
    items = [];
    saveCards();
    clearCards();
};

CART.saveCurrentCard = function (this_) {
    var $currentCard = $(this_).parents('.card'),
        data = {
            id: $currentCard.data('id'),
            image: $currentCard.find('.person-img').attr('src'),
            name: $currentCard.find('.person-name').text(),
            url: $currentCard.data('url')
        },
        html = Mustache.render(TMPL_CARD, data);

    // FIXME: existance check를 좀 더 엄밀하게
    if (items.indexOf(html) != -1) {
        alert('already exists');
        return;
    }

    prependCard(html);
    items.push(html);
    saveCards();
};

CART.removeCard = function (that) {
    var $this = $(that).parents('.card');
    items.splice(items.indexOf($this.html()), 1);
    saveCards();
    $this.remove();
};

}());
