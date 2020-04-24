<template>
  <div class="cb-launcher">
    This is CodeBang Lanucher.
  </div>
</template>

<script>
import connector from '../connector.js'

export default {
    name: 'LaunchManager',
    props: {
        coursework: Object,
    },
    data() {
        return {
            editor: null
        }
    },
    mounted() {
        connector.$on( 'api-login', (success) => {
            this.isAuthenticated = success
            if (success)
                connector.getLogon()
        } )
    },
    methods: {
        handleNewFile: function () {
            this.editor.setValue(
                '#include <stdio.h>\n\nint main(int argc, char *argv[])\n' +
                    '{\n    printf("Hello World\\n");\n    return 0;\n}')
            this.editor.selection.clearSelection()
            this.editor.gotoLine(1);
            this.editor.focus()
        }
    }
}
</script>

<style>
</style>
