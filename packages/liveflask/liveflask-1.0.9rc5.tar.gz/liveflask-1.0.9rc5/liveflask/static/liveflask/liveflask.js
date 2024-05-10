///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// INITIALIZERS
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

window.liveflask = {
    components: [],
    first: function () {
        return this.components.length > 0 ? this.components[0] : null;
    },
    find: function (id) {
        return this.components.find(component => component.data.key === id) || null;
    },
    get_by_name: function (name) {
        return this.components.filter(component => component.class === name);
    },
    all: function () {
        return this.components;
    }
}

document.querySelectorAll('[data-component]').forEach(el => {
    let live_flask_children = [];
    let elementsWithDataLoading = el.querySelectorAll('[data-loading]');

    el.__liveflask = JSON.parse(el.getAttribute('data-snapshot'));
    el.removeAttribute('data-snapshot')


    elementsWithDataLoading.forEach(element => {
        console.log("Element with data-loading: ", element);
        element.style.display = "none";
    });


    init_model(el)
    init_action(el)
    init_polling(el)


    el.__liveflask.set = function (key, value) {
        el.__liveflask[key] = value
        send_request(el, {update_property: [key, value]}, undefined)
    }

    window.liveflask.components.push(el.__liveflask);

    // register event named liveflask:initialized
    document.dispatchEvent(new CustomEvent('liveflask:initialized', {detail: el.__liveflask, target: el}))
    init_inits(el)

})