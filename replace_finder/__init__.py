from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtWidgets import QApplication
from fman import ApplicationCommand, show_alert
import fman.url
import fman.fs
import traceback
import subprocess

class ReplaceFinder(ApplicationCommand):
    aliases = ['Replace Finder']

    def __init__(self, *args, **kwargs):
        super(ReplaceFinder, self).__init__(*args, **kwargs)

        app = QApplication.instance()
        self.fileOpenListener = FileOpenListener(app, self.window)
        # When plugins are reloaded (using 'Reload plugins'), the object is not on the main thread by default.
        # The event filter will only be called if the object is on the main thread.
        self.fileOpenListener.moveToThread(app.thread())
        app.installEventFilter(self.fileOpenListener)
        
    def __call__(self):
        subprocess.check_call(['defaults', 'write', '-g', 'NSFileViewer', '-string', 'io.fman.fman'])
        show_alert('"Show in Finder" should now open fman instead. Go fman!\n\n'
            'If this doesn\'t take effect in some app, restart that app.')

    def __del__(self):
        QApplication.instance().removeEventFilter(self.fileOpenListener)
        self.fileOpenListener.deleteLater()

class FileOpenListener(QObject):
    def __init__(self, parent, window):
        super(FileOpenListener, self).__init__(parent)
        self.window = window

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FileOpen:
            self.safe_file_opened(event.url().toString())
            return False
        else:
            return QObject.eventFilter(self, obj, event)

    def safe_file_opened(self, url):
        try:
            self.file_opened(url)
        except:
            # Display a nice error message. (If we don't, fman will display a generic error and swallow the details.)
            show_alert('Error opening path: %s\n\n%s' % (url, traceback.format_exc()))

    def file_opened(self, url):
        if not fman.fs.exists(url):
            show_alert('Path doesn\'t exist: ' + fman.url.as_human_readable(url))
            return
        
        target_pane = self.window.get_panes()[0]
        
        if fman.fs.is_dir(url):
            target_pane.set_path(url)
        else:
            target_dir = fman.url.dirname(url)
            
            def directory_opened():
                # TODO: if a file is created outside of fman, and fman is already showing the containing folder,
                #       an exception will be thrown on `place_cursor_at` because fman didn't refresh yet.
                #       Calling `reload` doesn't help - it is async apparently.
                # target_pane.reload()
                target_pane.place_cursor_at(url)
            
            target_pane.set_path(target_dir, directory_opened)