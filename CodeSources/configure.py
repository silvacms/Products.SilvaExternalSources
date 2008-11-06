configuration = {
    'cs_you_tube': {
        'id': 'cs_you_tube',
        'title': 'YouTube video',
        'render_id': 'youtube_source',
        'desc': "Code Source to embed YouTube videos",
        'cacheable': True,
        'elaborate': False,
    },
    'cs_google_calendar': {
        'id': 'cs_google_calendar',
        'title': 'Google Calendar',
        'render_id': 'google_calendar_source',
        'desc': 'Code Source to embed a public Google Calendar.',
        'cacheable': True,
        'elaborate': False,
    },
    #cs_toc should eventually replace cs_multitoc, since it is unified
    # with the toc_rendering adapter, and will replace the TOC element
    'cs_toc': {
        'id': 'cs_toc',
        'title': 'TOC',
        'render_id': 'toc',
        'desc': 'Displays a listing of items contained in folders and/or publications. (replaces the TOC element)',
        'cacheable': False,
        'elaborate': False,
    },
   'cs_multitoc': {
        'id': 'cs_multitoc',
        'title': 'MultiTOC',
        'render_id': 'multi_toc',
        'desc': 'Displays a listing of items contained in folders and/or publications.',
        'cacheable': False,
        'elaborate': False,
    },
    'cs_google_maps': {
        'id': 'cs_google_maps',
        'title': 'Code Source Google Maps iFrame',
        'render_id': 'google_maps_source',
        'desc': 'Code Source for Google Maps iFrame.',
        'cacheable': True,
        'elaborate': False,
    },
    'cs_network_image': {
        'id': 'cs_network_image',
        'title': 'Network Image',
        'render_id': 'netimage',
        'desc': 'Insert an image from the network with a link and/or tooltip.',
        'cacheable': True,
        'elaborate': False,
    },
    'cs_ms_video': {
        'id': 'cs_ms_video',
        'title': 'MS Video',
        'render_id': 'video_script',
        'desc': 'Embeds a Window Media Player movie.',
        'cacheable': True,
        'elaborate': False,
    },
    'cs_quicktime': {
        'id': 'cs_quicktime',
        'title': 'Quicktime',
        'render_id': 'video_script',
        'desc': 'Embedder for a Quicktime movie with configuration parameters.',
        'cacheable': True,
        'elaborate': False,
    },
    'cs_related_info': {
        'id': 'cs_related_info',
        'title': 'Related info',
        'render_id': 'capsule',
        'desc': 'Provide related info and crosslinks.',
        'cacheable': True,
        'elaborate': False,
    },
    'cs_flash': {
        'id': 'cs_flash',
        'title': 'Flash',
        'render_id': 'flash_script',
        'desc': 'Embeds a Flash movie in a page using parameters.',
        'cacheable': False,
        'elaborate': False,
    },
    'cs_encaptionate': {
        'id': 'cs_encaptionate',
        'title': 'Encaptionated image',
        'render_id': 'capsule',
        'desc': 'Insert an image with title, link, caption, and/or credit.',
        'cacheable': True,
        'elaborate': False,
    },
    'cs_java_applet': {
        'id': 'cs_java_applet',
        'title': 'Java Applet',
        'render_id': 'java_script',
        'desc': 'Embeds a Java applet with parameters using the HTML applet tag.',
        'cacheable': True,
        'elaborate': False,
    },
    'cs_java_plugin': {
        'id': 'cs_java_plugin',
        'title': 'Java Plugin',
        'render_id': 'java_script',
        'desc': 'Embeds a Java applet with the Java plug-in mechanism.',
        'cacheable': True,
        'elaborate': False,
    },
    'cs_search_field': {
        'id': 'cs_search_field',
        'title': 'Search Field',
        'render_id': 'layout',
        'desc': 'Inserts a search field in a document. Requires SilvaFind.',
        'cacheable': True,
        'elaborate': False,
    },
    'cs_flash_source': {
        'id': 'cs_flash_source',
        'title': 'Flash Source',
        'render_id': 'embedder',
        'desc': 'This Code Source embeds a Flash file (swf or flv) in a page and provides a form for easy parameter configuration.',
        'cacheable': True,
        'elaborate': False,
    },
    'cs_portlet_element': {
        'id': 'cs_portlet_element',
        'title': 'Portlet Element',
        'render_id': 'portlet_element',
        'desc': 'Code Source to include Silva Documents within other Silva Documents.',
        'cacheable': True,
        'elaborate': False,
    },
}
