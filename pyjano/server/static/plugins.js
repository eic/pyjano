let plugins = [
        {'info-source': {
            'sel':0
            }}
    ];
    function ClearInfoClass() {
        $('.info-source').removeClass('bg-light')
    }

    function ClearConfigInfoClass() {
        $('.config-info-source').removeClass('bg-light')
    }

    function HideDocumentation() {
        $('.help-view').hide()
    }

    function HideConfigs() {
        $('.plugin-config-set').hide()
    }

    function activatePluginsGui() {
        console.log('plugins template initialized');
        $('.info-source').click(function() {
            ClearInfoClass();
            ClearConfigInfoClass();
            HideDocumentation();
            HideConfigs();
            $(this).addClass('bg-light');
            let pluginName = $(this).data("name");
            $(`#${pluginName}-help`).show();
            $(`#${pluginName}-config-set`).show();
        });
        $('.config-info-source').click(function() {
            ClearInfoClass();
            ClearConfigInfoClass();
            HideDocumentation();
            $(this).addClass('bg-light');
            let pluginName = $(this).data("name");
            $(`#${pluginName}-help`).show();
            $(`#${pluginName}-config-set`).show();
        });

        $('.plugin-checkbox').change(function () {
            let el = $(this);
            let name = el.val();
            let check = el.prop('checked');
            console.log("Change: " + name + " to " + check);
            pluginsToConfig();
        });

        $('.plugin-param-checkbox').change(function(){pluginsToConfig();});
        $('.plugin-param-input').change(function(){pluginsToConfig();});
        pluginsToConfig();
    }

    function pluginsToConfig() {
        let plugins = [];
        let plugins_by_name = {};
        $('.plugin-checkbox:checked').each(function() {
            console.log(this);
            plugins.push(this.dataset.name);
            plugins_by_name[this.dataset.name] = {};
        });

        // plugin-param-checkbox plugin-param-input


        let output = "";
        for(let plugin of plugins) {
            let parameters = [];
            let parameters_by_name = [];

            console.log(`Looking parameters for ${plugin}`);

            $(`input.plugin-param-checkbox[data-plugin=${plugin}]:checked`).each(function() {
                //console.log(this);
                let full_name = this.dataset.name;
                parameters.push(full_name);

                for (let parameter of parameters) {
                    let value = $(`input.plugin-param-input[data-name='${parameter}']`).first().val();
                    parameters_by_name[full_name] = value;
                    output += `${full_name}=${value} `;
                }

                //console.log(this.dataset.name);

                plugins_by_name[plugin].parameters = parameters_by_name;
            });
            output += plugin + " ";
        }
        console.log(output);
        $('#config-help').text(output)
    }