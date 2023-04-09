function removeItem(itemName) {
    fetch(`/cart/${itemName.replace(' ', '-')}`, {method: 'DELETE'})
        .then(() => window.location.href = '/payment');
}