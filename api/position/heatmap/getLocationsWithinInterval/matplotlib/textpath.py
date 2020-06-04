from collections import OrderedDict
import functools
import logging
import urllib.parse

import numpy as np

from matplotlib import _text_layout, cbook, dviread, font_manager, rcParams
from matplotlib.font_manager import FontProperties, get_font
from matplotlib.ft2font import LOAD_NO_HINTING, LOAD_TARGET_LIGHT
from matplotlib.mathtext import MathTextParser
from matplotlib.path import Path
from matplotlib.transforms import Affine2D

_log = logging.getLogger(__name__)


class TextToPath:
    """A class that converts strings to paths."""

    FONT_SCALE = 100.
    DPI = 72

    def __init__(self):
        self.mathtext_parser = MathTextParser('path')
        self._texmanager = None

    def _get_font(self, prop):
        """
        Find the `FT2Font` matching font properties *prop*, with its size set.
        """
        fname = font_manager.findfont(prop)
        font = get_font(fname)
        font.set_size(self.FONT_SCALE, self.DPI)
        return font

    def _get_hinting_flag(self):
        return LOAD_NO_HINTING

    def _get_char_id(self, font, ccode):
        """
        Return a unique id for the given font and character-code set.
        """
        return urllib.parse.quote('{}-{}'.format(font.postscript_name, ccode))

    def _get_char_id_ps(self, font, ccode):
        """
        Return a unique id for the given font and character-code set (for tex).
        """
        ps_name = font.get_ps_font_info()[2]
        char_id = urllib.parse.quote('%s-%d' % (ps_name, ccode))
        return char_id

    @cbook.deprecated(
        "3.1",
        alternative="font.get_path() and manual translation of the vertices")
    def glyph_to_path(self, font, currx=0.):
        """Convert the *font*'s current glyph to a (vertices, codes) pair."""
        verts, codes = font.get_path()
        if currx != 0.0:
            verts[:, 0] += currx
        return verts, codes

    def get_text_width_height_descent(self, s, prop, ismath):
        if rcParams['text.usetex']:
            texmanager = self.get_texmanager()
            fontsize = prop.get_size_in_points()
            w, h, d = texmanager.get_text_width_height_descent(s, fontsize,
                                                               renderer=None)
            return w, h, d

        fontsize = prop.get_size_in_points()
        scale = fontsize / self.FONT_SCALE

        if ismath:
            prop = prop.copy()
            prop.set_size(self.FONT_SCALE)

            width, height, descent, trash, used_characters = \
                self.mathtext_parser.parse(s, 72, prop)
            return width * scale, height * scale, descent * scale

        font = self._get_font(prop)
        font.set_text(s, 0.0, flags=LOAD_NO_HINTING)
        w, h = font.get_width_height()
        w /= 64.0  # convert from subpixels
        h /= 64.0
        d = font.get_descent()
        d /= 64.0
        return w * scale, h * scale, d * scale

    @cbook._delete_parameter("3.1", "usetex")
    def get_text_path(self, prop, s, ismath=False, usetex=False):
        """
        Convert text *s* to path (a tuple of vertices and codes for
        matplotlib.path.Path).

        Parameters
        ----------
        prop : `matplotlib.font_manager.FontProperties` instance
            The font properties for the text.

        s : str
            The text to be converted.

        ismath : {False, True, "TeX"}
            If True, use mathtext parser.  If "TeX", use tex for renderering.

        usetex : bool, optional
            If set, forces *ismath* to True.  This parameter is deprecated.

        Returns
        -------
        verts, codes : tuple of lists
            *verts*  is a list of numpy arrays containing the x and y
            coordinates of the vertices. *codes* is a list of path codes.

        Examples
        --------
        Create a list of vertices and codes from a text, and create a `Path`
        from those::

            from matplotlib.path import Path
            from matplotlib.textpath import TextToPath
            from matplotlib.font_manager import FontProperties

            fp = FontProperties(family="Humor Sans", style="italic")
            verts, codes = TextToPath().get_text_path(fp, "ABC")
            path = Path(verts, codes, closed=False)

        Also see `TextPath` for a more direct way to create a path from a text.
        """
        if usetex:
            ismath = "TeX"
        if ismath == "TeX":
            glyph_info, glyph_map, rects = self.get_glyphs_tex(prop, s)
        elif not ismath:
            font = self._get_font(prop)
            glyph_info, glyph_map, rects = self.get_glyphs_with_font(font, s)
        else:
            glyph_info, glyph_map, rects = self.get_glyphs_mathtext(prop, s)

        verts, codes = [], []

        for glyph_id, xposition, yposition, scale in glyph_info:
            verts1, codes1 = glyph_map[glyph_id]
            if len(verts1):
                verts1 = np.array(verts1) * scale + [xposition, yposition]
                verts.extend(verts1)
                codes.extend(codes1)

        for verts1, codes1 in rects:
            verts.extend(verts1)
            codes.extend(codes1)

        return verts, codes

    def get_glyphs_with_font(self, font, s, glyph_map=None,
                             return_new_glyphs_only=False):
        """
        Convert string *s* to vertices and codes using the provided ttf font.
        """

        if glyph_map is None:
            glyph_map = OrderedDict()

        if return_new_glyphs_only:
            glyph_map_new = OrderedDict()
        else:
            glyph_map_new = glyph_map

        xpositions = []
        glyph_ids = []
        for char, (_, x) in zip(s, _text_layout.layout(s, font)):
            char_id = self._get_char_id(font, ord(char))
            glyph_ids.append(char_id)
            xpositions.append(x)
            if char_id not in glyph_map:
                glyph_map_new[char_id] = font.get_path()

        ypositions = [0] * len(xpositions)
        sizes = [1.] * len(xpositions)

        rects = []

        return (list(zip(glyph_ids, xpositions, ypositions, sizes)),
                glyph_map_new, rects)

    def get_glyphs_mathtext(self, prop, s, glyph_map=None,
                            return_new_glyphs_only=False):
        """
        Parse mathtext string *s* and convert it to a (vertices, codes) pair.
        """

        prop = prop.copy()
        prop.set_size(self.FONT_SCALE)

        width, height, descent, glyphs, rects = self.mathtext_parser.parse(
            s, self.DPI, prop)

        if not glyph_map:
            glyph_map = OrderedDict()

        if return_new_glyphs_only:
            glyph_map_new = OrderedDict()
        else:
            glyph_map_new = glyph_map

        xpositions = []
        ypositions = []
        glyph_ids = []
        sizes = []

        for font, fontsize, ccode, ox, oy in glyphs:
            char_id = self._get_char_id(font, ccode)
            if char_id not in glyph_map:
                font.clear()
                font.set_size(self.FONT_SCALE, self.DPI)
                font.load_char(ccode, flags=LOAD_NO_HINTING)
                glyph_map_new[char_id] = font.get_path()

            xpositions.append(ox)
            ypositions.append(oy)
            glyph_ids.append(char_id)
            size = fontsize / self.FONT_SCALE
            sizes.append(size)

        myrects = []
        for ox, oy, w, h in rects:
            vert1 = [(ox, oy), (ox, oy + h), (ox + w, oy + h),
                     (ox + w, oy), (ox, oy), (0, 0)]
            code1 = [Path.MOVETO,
                     Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO,
                     Path.CLOSEPOLY]
            myrects.append((vert1, code1))

        return (list(zip(glyph_ids, xpositions, ypositions, sizes)),
                glyph_map_new, myrects)

    def get_texmanager(self):
        """Return the cached `~.texmanager.TexManager` instance."""
        if self._texmanager is None:
            from matplotlib.texmanager import TexManager
            self._texmanager = TexManager()
        return self._texmanager

    def get_glyphs_tex(self, prop, s, glyph_map=None,
                       return_new_glyphs_only=False):
        """Convert the string *s* to vertices and codes using usetex mode."""
        # Mostly borrowed from pdf backend.

        dvifile = self.get_texmanager().make_dvi(s, self.FONT_SCALE)
        with dviread.Dvi(dvifile, self.DPI) as dvi:
            page, = dvi

        if glyph_map is None:
            glyph_map = OrderedDict()

        if return_new_glyphs_only:
            glyph_map_new = OrderedDict()
        else:
            glyph_map_new = glyph_map

        glyph_ids, xpositions, ypositions, sizes = [], [], [], []

        # Gather font information and do some setup for combining
        # characters into strings.
        for x1, y1, dvifont, glyph, width in page.text:
            font, enc = self._get_ps_font_and_encoding(dvifont.texname)
            char_id = self._get_char_id_ps(font, glyph)

            if char_id not in glyph_map:
                font.clear()
                font.set_size(self.FONT_SCALE, self.DPI)
                # See comments in _get_ps_font_and_encoding.
                if enc is not None:
                    index = font.get_name_index(enc[glyph])
                    font.load_glyph(index, flags=LOAD_TARGET_LIGHT)
                else:
                    font.load_char(glyph, flags=LOAD_TARGET_LIGHT)
                glyph_map_new[char_id] = font.get_path()

            glyph_ids.append(char_id)
            xpositions.append(x1)
            ypositions.append(y1)
            sizes.append(dvifont.size / self.FONT_SCALE)

        myrects = []

        for ox, oy, h, w in page.boxes:
            vert1 = [(ox, oy), (ox + w, oy), (ox + w, oy + h),
                     (ox, oy + h), (ox, oy), (0, 0)]
            code1 = [Path.MOVETO,
                     Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO,
                     Path.CLOSEPOLY]
            myrects.append((vert1, code1))

        return (list(zip(glyph_ids, xpositions, ypositions, sizes)),
                glyph_map_new, myrects)

    @staticmethod
    @functools.lru_cache(50)
    def _get_ps_font_and_encoding(texname):
        tex_font_map = dviread.PsfontsMap(dviread.find_tex_file('pdftex.map'))
        font_bunch = tex_font_map[texname]
        if font_bunch.filename is None:
            raise ValueError(
                f"No usable font file found for {font_bunch.psname} "
                f"({texname}). The font may lack a Type-1 version.")

        font = get_font(font_bunch.filename)

        if font_bunch.encoding:
            # If psfonts.map specifies an encoding, use it: it gives us a
            # mapping of glyph indices to Adobe glyph names; use it to convert
            # dvi indices to glyph names and use the FreeType-synthesized
            # unicode charmap to convert glyph names to glyph indices (with
            # FT_Get_Name_Index/get_name_index), and load the glyph using
            # FT_Load_Glyph/load_glyph.  (That charmap has a coverage at least
            # as good as, and possibly better than, the native charmaps.)
            enc = dviread._parse_enc(font_bunch.encoding)
        else:
            # If psfonts.map specifies no encoding, the indices directly
            # map to the font's "native" charmap; so don't use the
            # FreeType-synthesized charmap but the native ones (we can't
            # directly identify it but it's typically an Adobe charmap), and
            # directly load the dvi glyph indices using FT_Load_Char/load_char.
            for charmap_code in [
                    1094992451,  # ADOBE_CUSTOM.
                    1094995778,  # ADOBE_STANDARD.
            ]:
                try:
                    font.select_charmap(charmap_code)
                except (ValueError, RuntimeError):
                    pass
                else:
                    break
            else:
                _log.warning("No supported encoding in font (%s).",
                             font_bunch.filename)
            enc = None

        return font, enc


text_to_path = TextToPath()


class TextPath(Path):
    """
    Create a path from the text.
    """

    def __init__(self, xy, s, size=None, prop=None,
                 _interpolation_steps=1, usetex=False,
                 *args, **kwargs):
        r"""
        Create a path from the text. Note that it simply is a path,
        not an artist. You need to use the `~.PathPatch` (or other artists)
        to draw this path onto the canvas.

        Parameters
        ----------
        xy : tuple or array of two float values
            Position of the text. For no offset, use ``xy=(0, 0)``.

        s : str
            The text to convert to a path.

        size : float, optional
            Font size in points. Defaults to the size specified via the font
            properties *prop*.

        prop : `matplotlib.font_manager.FontProperties`, optional
            Font property. If not provided, will use a default
            ``FontProperties`` with parameters from the
            :ref:`rcParams <matplotlib-rcparams>`.

        _interpolation_steps : integer, optional
            (Currently ignored)

        usetex : bool, optional
            Whether to use tex rendering. Defaults to ``False``.

        Examples
        --------
        The following creates a path from the string "ABC" with Helvetica
        font face; and another path from the latex fraction 1/2::

            from matplotlib.textpath import TextPath
            from matplotlib.font_manager import FontProperties

            fp = FontProperties(family="Helvetica", style="italic")
            path1 = TextPath((12,12), "ABC", size=12, prop=fp)
            path2 = TextPath((0,0), r"$\frac{1}{2}$", size=12, usetex=True)

        Also see :doc:`/gallery/text_labels_and_annotations/demo_text_path`.
        """
        # Circular import.
        from matplotlib.text import Text

        if args or kwargs:
            cbook.warn_deprecated(
                "3.1", message="Additional arguments to TextPath used to be "
                "ignored, but will trigger a TypeError %(removal)s.")

        if prop is None:
            prop = FontProperties()
        if size is None:
            size = prop.get_size_in_points()

        self._xy = xy
        self.set_size(size)

        self._cached_vertices = None
        s, ismath = Text(usetex=usetex)._preprocess_math(s)
        self._vertices, self._codes = text_to_path.get_text_path(
            prop, s, ismath=ismath)
        self._should_simplify = False
        self._simplify_threshold = rcParams['path.simplify_threshold']
        self._interpolation_steps = _interpolation_steps

    def set_size(self, size):
        """Set the text size."""
        self._size = size
        self._invalid = True

    def get_size(self):
        """Get the text size."""
        return self._size

    @property
    def vertices(self):
        """
        Return the cached path after updating it if necessary.
        """
        self._revalidate_path()
        return self._cached_vertices

    @property
    def codes(self):
        """
        Return the codes
        """
        return self._codes

    def _revalidate_path(self):
        """
        Update the path if necessary.

        The path for the text is initially create with the font size of
        `~.FONT_SCALE`, and this path is rescaled to other size when necessary.
        """
        if self._invalid or self._cached_vertices is None:
            tr = (Affine2D()
                  .scale(self._size / text_to_path.FONT_SCALE)
                  .translate(*self._xy))
            self._cached_vertices = tr.transform(self._vertices)
            self._invalid = False

    @cbook.deprecated("3.1")
    def is_math_text(self, s):
        """
        Returns True if the given string *s* contains any mathtext.
        """
        # copied from Text.is_math_text -JJL

        # Did we find an even number of non-escaped dollar signs?
        # If so, treat is as math text.
        dollar_count = s.count(r'$') - s.count(r'\$')
        even_dollars = (dollar_count > 0 and dollar_count % 2 == 0)

        if rcParams['text.usetex']:
            return s, 'TeX'

        if even_dollars:
            return s, True
        else:
            return s.replace(r'\$', '$'), False

    @cbook.deprecated("3.1", alternative="TextPath")
    def text_get_vertices_codes(self, prop, s, usetex):
        """
        Convert string *s* to a (vertices, codes) pair using font property
        *prop*.
        """
        # Mostly copied from backend_svg.py.
        if usetex:
            return text_to_path.get_text_path(prop, s, usetex=True)
        else:
            clean_line, ismath = self.is_math_text(s)
            return text_to_path.get_text_path(prop, clean_line, ismath=ismath)
