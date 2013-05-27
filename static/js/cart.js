(function () {

var namespace = 'cards-cart-v0.1',
    items = [],
    $cart = $('#cards-cart');

// TODO: Load the template from the server dynamically
var TMPL_CARD = '\
<div class="card card-small" data-id="{{id}}" data-url="{{url}}">\
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

    items = localStorage.getItem(namespace) || '{}';

    try {
        items = JSON.parse(items);
    } catch (e) {
        if (console && console.error) {
            console.error('error loading cart items');
        }
    }

    $.each(items, function (id, item) {
        prependCard(item);
    });
}

function prependCard(data) {
    var html = card(data),
        $card = $(html).appendTo($cart);
    $card.find('.person-img').clipImage();
    CART.updateStatus($card);
}

function saveCards() {
    localStorage.setItem(namespace, JSON.stringify(items));
}

function isExists(id) {
    return typeof items[id] != 'undefined';
}

function card(data) {
    return Mustache.render(TMPL_CARD, data);
}

CART.clearCart = function () {
    items = {};
    saveCards();
    clearCards();
};

CART.saveCurrentCard = function (that) {
    var $currentCard = $(that).parents('.card'),
        data = {
            id: $currentCard.data('id'),
            image: $currentCard.find('.person-img').attr('src'),
            name: $currentCard.find('.person-name').text(),
            url: $currentCard.data('url')
        };

    if (isExists(data.id)) {
        alert('already exists');
        return;
    }

    items[data.id] = data;
    prependCard(data);
    saveCards();
};

CART.removeCard = function (that) {
    var $this = $(that).parents('.card');
    delete items[$this.data('id')];
    saveCards();
    $this.remove();
    CART.updateStatus();
};

CART.updateStatus = function () {
    var $cards = $('.card');
    $cards.each(function () {
        var $this = $(this);
        $this.toggleClass('favorited', isExists($this.data('id')));
    });
};

}());
