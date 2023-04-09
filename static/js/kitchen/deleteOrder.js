function deleteOrder(id) {
    fetch(`/kitchen/${id}`, {
        method: 'DELETE'
    }).then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            alert('Failed to delete order');
        }
    }).catch(error => {
        alert('Failed to delete order');
    });
}
