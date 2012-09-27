(function() {
  // Load plugin specific language pack
  tinymce.PluginManager.requireLangPack('commonplacer');

  tinymce.create('tinymce.plugins.CommonplacerPlugin', {
    /**
     * Initializes the plugin, this will be executed after the plugin has
     * been created.
     * This call is done before the editor instance has finished it's
     * initialization so use the onInit eventof the editor instance to
     * intercept that event.
     *
     * @param {tinymce.Editor} ed Editor instance that the plugin is
     *  initialized in.
     * @param {string} url Absolute URL to where the plugin is located.
     */
    init : function(ed, url) {
      var CP = 'cp';
      var LG = 'lg';
      var LN = 'ln';
      var NODE_NAME = 'SPAN';

      // Register the line number command
      ed.addCommand('mceCommonplacerLineNumber', function() {
        ed.formatter.register(LN, {
          attributes : {'class' : CP + ' ' + LN},
          inline : 'span'
        });

        ed.formatter.toggle(LN);
      });

      // Register line number button
      ed.addButton('commonplacerLineNumber', {
        title : 'commonplacer.linenumber',
        cmd : 'mceCommonplacerLineNumber',
        image : url + '/img/linenumber.gif'
      });

      // Register the line gloss command
      ed.addCommand('mceCommonplacerLineGloss', function() {
        ed.formatter.register(LG, {
          attributes : {'class' : CP + ' ' + LG},
          inline : 'span'
        });

        ed.formatter.toggle(LG);
      });

      // Register the line gloss button
      ed.addButton('commonplacerLineGloss', {
        title : 'commonplacer.linegloss',
        cmd : 'mceCommonplacerLineGloss',
        image : url + '/img/linegloss.gif'
      });

      ed.onInit.add(function() {
        ed.dom.loadCSS(url + '/css/default.css');
      });

      // Add a node change handler, selects the button in the UI when a
      // commonplacer style is selected
      ed.onNodeChange.add(function(ed, cm, n) {
        cm.setActive('commonplacerLineNumber',
                     n.nodeName == NODE_NAME
                     && n.getAttribute('class').indexOf(LN) >= 0);

        cm.setActive('commonplacerLineGloss',
                     n.nodeName == NODE_NAME
                     && n.getAttribute('class').indexOf(LG) >= 0);
      });
    },

    /**
     * Returns information about the plugin as a name/value array.
     * The current keys are longname, author, authorurl, infourl and
     * version.
     *
     * @return {Object} Name/value array containing information about the
     *  plugin.
     */
    getInfo : function() {
      return {
        longname : 'Commonplacer plugin',
        version : "1.0"
      };
    }
  });

  // Register plugin
  tinymce.PluginManager.add('commonplacer',
                            tinymce.plugins.CommonplacerPlugin);
})();
