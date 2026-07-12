document.addEventListener(
    "DOMContentLoaded",
    function()
    {

        const buttons = document.querySelectorAll(
            "button"
        );


        buttons.forEach(
            function(button)
            {

                button.addEventListener(
                    "click",
                    function()
                    {

                        button.disabled = true;

                        setTimeout(
                            function()
                            {
                                button.disabled = false;
                            },
                            1000
                        );

                    }
                );

            }
        );


    }
);