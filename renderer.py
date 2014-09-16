import cairo

def load_pieces():
    result = {}
    pieces = 'bknpqr'
    colors = 'bw'
    for color in colors:
        for piece in pieces:
            key = piece.upper() if color == 'w' else piece
            path = 'pieces/%s%s.png' % (color, piece)
            result[key] = cairo.ImageSurface.create_from_png(path)
    return result

class Renderer(object):
    def __init__(self):
        self.border = 8
        self.padding = 1
        self.margin = 25
        self.gutter = 50
        self.piece_size = 80
        self.flip = False
        self.white = (0.93, 0.82, 0.65)
        self.black = (0.65, 0.46, 0.32)
        self.pieces = load_pieces()
    def ij_to_xy(self, i, j):
        if self.flip:
            i = 7 - i
            j = 7 - j
        n = self.piece_size + self.padding
        x = self.margin + self.gutter + self.border + n * i
        y = self.margin + self.border + n * j
        return (x, y)
    def compute_size(self):
        size = 0
        size += self.piece_size * 8
        size += self.padding * 7
        size += self.border * 2
        size += self.margin * 2
        size += self.gutter
        return size
    def render_squares(self, dc):
        colors = [self.white, self.black]
        for j in range(8):
            for i in range(8):
                index = (i + j) % 2
                dc.set_source_rgb(*colors[index])
                x, y = self.ij_to_xy(i, j)
                dc.rectangle(x, y, self.piece_size, self.piece_size)
                dc.fill()
    def render_labels(self, dc):
        size = self.compute_size()
        dc.set_font_size(36)
        dc.set_source_rgb(0, 0, 0)
        for i in range(8):
            x, y = self.ij_to_xy(i, 0)
            x += self.piece_size / 2
            y = self.margin + self.gutter / 2
            label = chr(ord('A') + i)
            tw, th = dc.text_extents(label)[2:4]
            dc.move_to(x - tw / 2, size - y + th / 2)
            dc.show_text(label)
        for j in range(8):
            x, y = self.ij_to_xy(0, j)
            x = self.margin + self.gutter / 2
            y += self.piece_size / 2
            label = str(8 - j)
            tw, th = dc.text_extents(label)[2:4]
            dc.move_to(x - tw / 2, y + th / 2)
            dc.show_text(label)
    def render_piece(self, dc, i, j, piece):
        x, y = self.ij_to_xy(i, j)
        dc.set_source_surface(self.pieces[piece], x, y)
        dc.paint()
    def render_pieces(self, dc, fen):
        ranks = fen.split()[0].split('/')
        for j, rank in enumerate(ranks):
            i = 0
            for piece in rank:
                if piece.isdigit():
                    i += int(piece)
                else:
                    self.render_piece(dc, i, j, piece)
                    i += 1
    def render_background(self, dc):
        m = self.margin
        g = self.gutter
        size = self.compute_size()
        dc.set_source_rgb(1, 1, 1)
        dc.paint()
        dc.set_source_rgb(0, 0, 0)
        dc.rectangle(m + g, m, size - m * 2 - g, size - m * 2 - g)
        dc.fill()
    def render(self, fen):
        self.flip = fen.split()[1].lower() == 'b'
        size = self.compute_size()
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, size, size)
        dc = cairo.Context(surface)
        self.render_background(dc)
        self.render_squares(dc)
        self.render_pieces(dc, fen)
        self.render_labels(dc)
        return surface

def main():
    fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    fen = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2'
    renderer = Renderer()
    surface = renderer.render(fen)
    surface.write_to_png('output.png')

if __name__ == '__main__':
    main()
