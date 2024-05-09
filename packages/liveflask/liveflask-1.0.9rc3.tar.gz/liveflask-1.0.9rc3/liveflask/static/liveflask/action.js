///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ACTIONS & EVENTS
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function init_action(el) {
    let component_name = el.__liveflask['class']
    let retrieved_actions = attr_beginswith('data-action', el);
    //console.log(retrieved_actions)
    el.__liveflask['actions'] = [];
    let current_component;

    retrieved_actions.forEach(i => {
        current_component = i.parentNode.closest('[data-component]').getAttribute("data-component");
        if (current_component !== component_name) return;
        el.__liveflask['actions'].push(i)
    })


    el.__liveflask['actions'].forEach(i => {
        let property;
        let value;
        let modifier;


        [property, modifier, value] = get_model_prop_value(i, "data-action")

        if (!i.__data_action_click_registered) {
            i.addEventListener('click', event => {
                let method = property.split("(")[0];
                let args;
                try {
                    args = replace_undefined(property).match(/\(([^)]+)\)/)[1];
                    // Love this one console.log(args)
                } catch (e) {
                    args = "__NOVAL__"
                }

                if (i.hasAttribute('data-action-confirm')) {
                    if (confirm(i.getAttribute("data-action-confirm"))) {
                        send_request(el, {'method': method, "args": args}, i)
                    } else {
                        return false
                    }
                } else {
                    send_request(el, {'method': method, "args": args}, i)
                }

            })
            i.__data_action_click_registered = true
        }
    })


}

