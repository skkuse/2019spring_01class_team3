function left_list_change(id) {

    if (id == "select-cat") {
        document.getElementById("select-cat").style.color = 'black';
        document.getElementById("select-brand").style.color = '#6c757d99';

        document.getElementById("list-brand").style.display = 'none';
        document.getElementById("list-cat").style.display = 'block';

    } else {
        document.getElementById("select-brand").style.color = 'black';
        document.getElementById("select-cat").style.color = '#6c757d99';

        document.getElementById("list-brand").style.display = 'block';
        document.getElementById("list-cat").style.display = 'none';
    }

}