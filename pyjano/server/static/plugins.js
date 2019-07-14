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
        });
    }
