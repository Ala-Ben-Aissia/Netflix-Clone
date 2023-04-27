class PlaylistMixin():
    title = None
    template_name = 'playlists/playlist_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.title is not None:
            context['title'] = self.title
        return context
 