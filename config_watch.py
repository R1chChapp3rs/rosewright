#! /usr/bin/env python

import PIL.Image
import PIL.ImageChops
import sys
import os
import getopt
import locale

help = """
config_watch.py

This script generates the resources and code tables needed to compile
a watch face with a particular set of hands.  It must be run before
compiling.

config_watch.py [opts]

Options:

    -s style
        Specifies the watch style.  The following styles are available:
          %(watchStyles)s

    -H style
        Overrides the hand style.  The following styles are available:
          %(handStyles)s

    -F style
        Overrides the face style.  The following styles are available:
          %(faceStyles)s

    -S
        Suppress the second hand if it is defined.

    -b
        Enable a quick buzz at the top of the hour.

    -c
        Enable chronograph mode (if the selected hand style includes
        chrono hands).  This builds the watch as a standard app,
        instead of as a watch face, to activate the chronograph
        buttons.

    -i
        Invert the hand color, for instance to apply a set of watch
        hands meant for a white face onto a black face.

    -d
        Compile for debugging.  Specifically this enables "fast time",
        so the hands move quickly about the face of the watch.

    -l locale
        Specifies the locale (for the day-of-week names).  Use a
        C-style local string such as en_US or de_DE.  The default is
        the current locale.
        
"""

def usage(code, msg = ''):
    watchStyles = watches.keys()
    watchStyles.sort()
    watchStyles = ' '.join(watchStyles)
    handStyles = hands.keys()
    handStyles.sort()
    handStyles = ' '.join(handStyles)
    faceStyles = faces.keys()
    faceStyles.sort()
    faceStyles = ' '.join(faceStyles)
    print >> sys.stderr, help % {
        'watchStyles' : watchStyles,
        'handStyles' : handStyles,
        'faceStyles' : faceStyles,
        }
    print >> sys.stderr, msg
    sys.exit(code)


# The default center for placing hands on the watch face, if not
# otherwise specified in the centers tables below.
centerX, centerY = 144 / 2, 168 / 2

# Table of watch styles.  A watch style is a combination of a hand
# style and face style, and a unique identifier.  For each style,
# specify the following:
#
#    name, handStyle, faceStyle, uuid
#
#  Where:
#
#   name      - the full name for this watch.
#   handStyle - the default hand style for this watch.
#   faceStyle - the default face style for this watch.
#   uuid      - the UUID to assign to this watch.
#
watches = {
    'a' : ('Rosewright A', 'a', 'a', [0xA4, 0x9C, 0x82, 0xFD, 0x83, 0x0E, 0x48, 0xB4, 0xA8, 0x2E, 0x9C, 0xF8, 0xDA, 0x77, 0xF4, 0xC5]),
    'b' : ('Rosewright B', 'b', 'b', [0xA4, 0x9C, 0x82, 0xFD, 0x83, 0x0E, 0x48, 0xB4, 0xA8, 0x2E, 0x9C, 0xF8, 0xDA, 0x77, 0xF4, 0xC6]),
    'c' : ('Rosewright Chronograph', 'c', 'c', [0xA4, 0x9C, 0x82, 0xFD, 0x83, 0x0E, 0x48, 0xB4, 0xA8, 0x2E, 0x9C, 0xF8, 0xDA, 0x77, 0xF4, 0xC7]),
    }
    

# Table of hand styles.  For each style, specify the following for
# each hand type.  Bitmapped hands will have bitmapParams defined and
# vectorParams None; vector hands will have vectorParams defined and
# bitmapParams None.  It is legal to have both bitmapParams and
# vectorParams defined for a given hand.
#
#    hand, bitmapParams, vectorParams
#
#  For bitmapParams:
#     (filename, colorMode, asymmetric, pivot, scale)
#
#   hand - the hand type being defined.
#   filename - the png image that defines this hand, pointing upward.
#   colorMode - indicate how the colors in the png file are to be interpreted:
#       'b'  - black pixels are drawn as black, white pixels are ignored.
#       'w'  - white pixels are drawn as white, black pixels are ignored.
#       '-b' - black pixels are drawn as white, white pixels are ignored.
#       '-w' - white pixels are drawn as black, black pixels are ignored.
#       't'  - opaque pixels are drawn in their own color,
#              transparent pixels are ignored.  This doubles the
#              resource cost.
#       '-t' - opaque pixels are drawn in their opposite color,
#              transparent pixels are ignored.  This doubles the
#              resource cost.
#       In addition, if any of the above is suffixed with '%', it
#       means to dither the grayscale levels in the png file to
#       produce the final black or white color pixel.  Without this
#       symbol, the default is to use thresholding.
#   asymmetric - false if the hand is left/right symmetric and can be
#       drawn mirrored, or false if it must be drawn without
#       mirroring, which doubles the resource cost again.
#   pivot - the (x, y) pixel point of the center of rotation of the
#       hand in its image.
#   scale - a scale factor for reducing the hand to its final size.
#
#  For vectorParams:
#     [(fillType, points), (fillType, points), ...]
#
#   fillType - Specify the type of the drawing:
#       'b'  - black unfilled stroke
#       'w'  - white unfilled stroke
#       'bb' - black stroke filled with black
#       'bw' - black stroke filled with white
#       'wb' - white stroke filled with black
#       'ww' - white stroke filled with white
#   points - a list of points in the vector.  Draw the hand in the
#       vertical position, from the pivot at (0, 0).
#

hands = {
    'a' : [('hour', ('a_hour_hand.png', 'b', False, (78, 410), 0.12), None),
           ('minute', ('a_minute_hand.png', 'b', True, (37, 557), 0.12), None),
           ('second', ('a_second_hand.png', 'b', False, (37, -28), 0.12),
            [('b', [(0, -5), (0, -70)])]),
           ],
    'b' : [('hour', ('b_hour_hand.png', 'b', False, (33, 211), 0.27), None),
           ('minute', ('b_minute_hand.png', 'b', False, (24, 280), 0.27), None),
           ('second', ('b_second_hand.png', 'b', False, (33, -23), 0.27),
            [('b', [(0, -5), (0, -75)]),
             ]),
           ],
    'c' : [('hour', ('c_hour_hand.png', 't%', False, (59, 434), 0.14), None),
           ('minute', ('c_minute_hand.png', 't%', False, (38, 584), 0.14), None),
           ('second', ('c_chrono1_hand.png', 'w', False, (32, -27), 0.14), 
            [('w', [(0, -2), (0, -26)]),
             ]),
           ('chrono_minute', ('c_chrono2_hand.png', 'w', False, (37, 195), 0.14), None),
           #('chrono_minute', None, [('ww', [(0, -4), (-1, -6), (-2, -9), (-2, -14), (-0, -26), (2, -14), (2, -9), (1, -6)]),]),
           ('chrono_second', ('c_second_hand.png', 'w', False, (41, -29), 0.14),
            [('w', [(0, -4), (0, -88)]),
             ]),
           ],
    }

# Table of face styles.  For each style, specify the following:
#
#    filename, dayCard, dateCard, centers
#
#  Where:
#
#   filename  - the background image for the face.
#   dayCard   - the (x, y) position of the "day of week" card, or None.
#   dateCard  - the (x, y) position of the "date of month" card, or None.
#   centers   - a list of [(hand, x, y)] to indicate the position for
#               each kind of watch hand.  If the list is empty or a
#               hand is omitted, the default is the center.  This also
#               defines the stacking order of the hands--any
#               explicitly listed hands are drawn in the order
#               specified, followed by all of the implicit hands in
#               the usual order.
#

faces = {
    'a' : ('a_face.png', None, (106, 82), []),
    'b' : ('b_face.png', (52, 109), (92, 109), []),
    'c' : ('c_face.png', None, None, [('chrono_minute', 115, 84), ('second', 29, 84)]),
    }

makeChronograph = False
showSecondHand = False
suppressSecondHand = False
enableHourBuzzer = False
showChronoMinuteHand = False
showChronoSecondHand = False
dayCard = None
dateCard = None

# The number of subdivisions around the face for each kind of hand.
# Increase these numbers to show finer movement; decrease them to save
# resource memory.
numSteps = {
    'hour' : 48,
    'minute' : 60,
    'second' : 60,
    'chrono_minute' : 30,
    'chrono_second' : 60,
    }

# The threshold level for dropping to 1-bit images.
threshold = 127
thresholdMap = [0] * (256 - threshold) + [255] * (threshold)

# Attempt to determine the directory in which we're operating.
rootDir = os.path.dirname(__file__) or '.'
srcDir = os.path.join(rootDir, 'resources/src')

def parseColorMode(colorMode):
    paintBlack = False
    useTransparency = False
    invertColors = False
    dither = False
    blackToken, whiteToken = 'b', 'w'

    inverted = False
    if colorMode[0] == '-':
        inverted = True
        colorMode = colorMode[1:]
    if invertHands:
        inverted = not inverted

    if inverted:
        invertColors = True
        blackToken, whiteToken = 'w', 'b'

    if colorMode[0] == blackToken:
        # Black is the foreground color.
        invertColors = not invertColors
        paintBlack = True
    elif colorMode[0] == whiteToken:
        # White is the foreground color.
        paintBlack = False
    elif colorMode[0] == 't':
        invertColors = not invertColors
        paintBlack = True
        useTransparency = True

    if colorMode.endswith('%'):
        dither = True

    return paintBlack, useTransparency, invertColors, dither
        
def makeFaces():

    resourceStr = ''
    
    resourceEntry = """
    {
    "defName": "CLOCK_FACE",
    "file": "clock_faces/%(targetFilename)s",
    "type": "png"
    },"""    

    targetFilename, dayCard, dateCard, centers = faces[faceStyle]

    resourceStr += resourceEntry % {
        'targetFilename' : targetFilename,
        }

    return resourceStr

def makeVectorHands(generatedTable, hand, groupList):
    resourceStr = ''

    colorMap = {
        'b' : 'GColorBlack',
        'w' : 'GColorWhite',
        '' : 'GColorClear',
        }

    print >> generatedTable, "#define VECTOR_%s_HAND 1" % (hand.upper())
    print >> generatedTable, "struct VectorHandTable %s_hand_vector_table = {" % (hand)

    print >> generatedTable, "  %s, (struct VectorHandGroup[]){" % (len(groupList))
    for fillType, points in groupList:
        stroke = colorMap[fillType[0]]
        fill = colorMap[fillType[1:2]]
        print >> generatedTable, "  { %s, %s, { %s, (GPoint[]){" % (stroke, fill, len(points))
        for px, py in points:
            print >> generatedTable, "    { %s, %s }," % (px, py)
        print >> generatedTable, "  } } },"
    
    print >> generatedTable, "  }"
    print >> generatedTable, "};"

    return resourceStr

def makeBitmapHands(generatedTable, hand, sourceFilename, colorMode, asymmetric, pivot, scale):
    resourceStr = ''

    resourceEntry = """
    {
    "defName": "%(defName)s",
    "file": "clock_hands/%(targetFilename)s",
    "type": "png"
    },"""    

    handTableEntry = """  { RESOURCE_ID_%(symbolName)s, RESOURCE_ID_%(symbolMaskName)s, %(cx)s, %(cy)s, %(flip_x)s, %(flip_y)s, %(paintBlack)s },"""
    
    print >> generatedTable, "#define BITMAP_%s_HAND 1" % (hand.upper())
    print >> generatedTable, "struct BitmapHandTableRow %s_hand_bitmap_table[] = {" % (hand)

    source = PIL.Image.open('%s/clock_hands/%s' % (srcDir, sourceFilename))

    paintBlack, useTransparency, invertColors, dither = parseColorMode(colorMode)

    if useTransparency or source.mode.endswith('A'):
        source, sourceMask = source.convert('LA').split()
    else:
        source = source.convert('L')
        sourceMask = None

    # We must do the below operations with white as the foreground
    # color and black as the background color, because the
    # rotate() operation always fills with black, and getbbox() is
    # always based on black.  Also, the Pebble library likes to
    # use white as the foreground color too.  So, invert the image
    # if necessary to make white the foreground color.
    if invertColors:
        source = PIL.ImageChops.invert(source)

    # The mask already uses black as the background color, no need
    # to invert that.

    if sourceMask:
        # Ensure that the source image is black anywhere the mask
        # is black (sometimes there is junk in the original png
        # image outside of the alpha channel coverage that the
        # artist didn't even know about).
        black = PIL.Image.new('L', source.size, 0)
        source = PIL.Image.composite(source, black, sourceMask)

    # Center the source image on its pivot, and pad it with black.
    border = (pivot[0], pivot[1], source.size[0] - pivot[0], source.size[1] - pivot[1])
    size = (max(border[0], border[2]) * 2, max(border[1], border[3]) * 2)
    center = (size[0] / 2, size[1] / 2)
    large = PIL.Image.new('L', size, 0)
    large.paste(source, (center[0] - pivot[0], center[1] - pivot[1]))

    if useTransparency:
        largeMask = PIL.Image.new('L', size, 0)
        largeMask.paste(sourceMask, (center[0] - pivot[0], center[1] - pivot[1]))

    for i in range(numSteps[hand]):
        flip_x = False
        flip_y = False
        angle = i * 360.0 / numSteps[hand]

        # Check for quadrant symmetry, an easy resource-memory
        # optimization.  Instead of generating bitmaps for all 360
        # degrees of the hand, we may be able to generate the
        # first quadrant only (or the first half only) and quickly
        # flip it into the remaining quadrants.
        if not asymmetric:
            # If the hand is symmetric, we can treat the x and y
            # flips independently, and this means we really only
            # need a single quadrant.

            if angle > 90:
                # If we're outside of the first quadrant, maybe we can
                # just flip a first-quadrant hand into the appropriate
                # quadrant, and save a bit of resource memory.
                i2 = i
                if angle > 180:
                    # If we're in the right half of the circle, flip
                    # over from the left.
                    i = (numSteps[hand] - i)
                    flip_x = True
                    angle = i * 360.0 / numSteps[hand]

                if angle > 90 and angle < 270:
                    # If we're in the bottom half of the circle, flip
                    # over from the top.
                    i = (numSteps[hand] / 2 - i) % numSteps[hand]
                    flip_y = True
                    angle = i * 360.0 / numSteps[hand]
        else:
            # If the hand is asymmetric, then it's important not
            # to flip it an odd number of times.  But we can still
            # apply both flips at once (which is really a
            # 180-degree rotation), and this means we only need to
            # generate the right half, and rotate into the left.
            if angle >= 180:
                i -= (numSteps[hand] / 2)
                flip_x = True
                flip_y = True
                angle = i * 360.0 / numSteps[hand]

        symbolName = '%s_%s' % (hand.upper(), i)
        symbolMaskName = symbolName
        if useTransparency:
            symbolMaskName = '%s_%s_mask' % (hand.upper(), i)

        # Now we are ready to continue.  We might have decided to
        # flip this image from another image i, but we still need
        # to scale and rotate the source image now, if for no
        # other reason than to compute cx, cy.

        p = large.rotate(-angle, PIL.Image.BICUBIC, True)
        scaledSize = (int(p.size[0] * scale + 0.5), int(p.size[1] * scale + 0.5))
        p = p.resize(scaledSize, PIL.Image.ANTIALIAS)
        if not dither:
            p = p.point(thresholdMap)
        p = p.convert('1')

        cx, cy = p.size[0] / 2, p.size[1] / 2
        cropbox = p.getbbox()
        if useTransparency:
            pm = largeMask.rotate(-angle, PIL.Image.BICUBIC, True)
            pm = pm.resize(scaledSize, PIL.Image.ANTIALIAS)
            pm = pm.point(thresholdMap)
            pm = pm.convert('1')
            # In the useTransparency case, it's important to take
            # the crop from the alpha mask, not from the color.
            cropbox = pm.getbbox() 
            pm = pm.crop(cropbox)
        p = p.crop(cropbox)

        cx, cy = cx - cropbox[0], cy - cropbox[1]

        if not flip_x and not flip_y:
            # If this is not a flipped image, actually write it out.

            # We also require our images to be an even multiple of
            # 8 pixels wide, to make it easier to reverse the bits
            # horizontally.  This doesn't consume any extra
            # memory, however.
            w = 8 * ((p.size[0] + 7) / 8)
            if w != p.size[0]:
                p1 = PIL.Image.new('1', (w, p.size[1]), 0)
                p1.paste(p, (0, 0))
                p = p1
                if useTransparency:
                    p1 = PIL.Image.new('1', (w, p.size[1]), 0)
                    p1.paste(pm, (0, 0))
                    pm = p1

            # It's nice to show a hole in the center pivot.
            ## if cx >= 0 and cx < p.size[0] and cy >= 0 and cy < p.size[1]:
            ##     p.putpixel((cx, cy), 0)
            ##     if useTransparency:
            ##         pm.putpixel((cx, cy), 0)

            targetFilename = 'flat_%s_%s_%s.png' % (handStyle, hand, i)
            print targetFilename

            p.save('%s/clock_hands/%s' % (srcDir, targetFilename))
            resourceStr += resourceEntry % {
                'defName' : symbolName,
                'targetFilename' : targetFilename,
                }

            if useTransparency:
                targetMaskFilename = 'flat_%s_%s_%s_mask.png' % (handStyle, hand, i)
                print targetMaskFilename

                pm.save('%s/clock_hands/%s' % (srcDir, targetMaskFilename))
                resourceStr += resourceEntry % {
                    'defName' : symbolMaskName,
                    'targetFilename' : targetMaskFilename,
                    }

        print >> generatedTable, handTableEntry % {
            'index' : i,
            'symbolName' : symbolName,
            'symbolMaskName' : symbolMaskName,
            'cx' : cx,
            'cy' : cy,
            'flip_x' : int(flip_x),
            'flip_y' : int(flip_y),
            'paintBlack' : int(paintBlack),
            }

    print >> generatedTable, "};\n"

    return resourceStr

def makeHands(generatedTable):
    """ Generates the required resources and tables for the indicated
    hand style.  Returns resourceStr. """
    
    resourceStr = ''

    for hand, bitmapParams, vectorParams in hands[handStyle]:
        if hand == 'second':
            global showSecondHand
            showSecondHand = True
        elif hand == 'chrono_minute':
            global showChronoMinuteHand
            showChronoMinuteHand = True
        elif hand == 'chrono_second':
            global showChronoSecondHand
            showChronoSecondHand = True
            
        if bitmapParams:
            resourceStr += makeBitmapHands(generatedTable, hand, *bitmapParams)
        if vectorParams:
            resourceStr += makeVectorHands(generatedTable, hand, vectorParams)

    return resourceStr

def makeDates(generatedTable):
    print >> generatedTable, "const char *weekday_names[7] = {"
    for sym in [locale.ABDAY_1, locale.ABDAY_2, locale.ABDAY_3, locale.ABDAY_4, locale.ABDAY_5, locale.ABDAY_6, locale.ABDAY_7]:
        name = locale.nl_langinfo(sym)
        #name = name.decode('utf-8').upper().encode('utf-8')

        if '"' in name or name.encode('string_escape') != name:
            # The text has some fancy characters.  We can't just pass
            # string_escape, since that's not 100% C compatible.
            # Instead, we'll aggressively hexify every character.
            name = ''.join(map(lambda c: '\\x%02x' % (ord(c)), name))
        
        print >> generatedTable, '  \"%s\",' % (name)
    print >> generatedTable, "};\n"
        
def configWatch():
    generatedTable = open('%s/generated_table.c' % (srcDir), 'w')

    resourceStr = ''
    resourceStr += makeFaces()
    resourceStr += makeHands(generatedTable)

    makeDates(generatedTable)

    resourceIn = open('%s/resource_map.json.in' % (srcDir), 'r').read()
    resource = open('%s/resource_map.json' % (srcDir), 'w')

    print >> resource, resourceIn % {
        'generatedMedia' : resourceStr[:-1],
        }


    configIn = open('%s/generated_config.h.in' % (srcDir), 'r').read()
    config = open('%s/generated_config.h' % (srcDir), 'w')

    # Map the centers list into a dictionary of points for x and y.
    cxd = dict(map(lambda (hand, x, y): (hand, x), centers))
    cyd = dict(map(lambda (hand, x, y): (hand, y), centers))

    # Get the stacking orders of the hands too.
    implicitStackingOrder = ['hour', 'minute', 'second', 'chrono_minute', 'chrono_second']
    explicitStackingOrder = []
    for hand, x, y in centers:
        implicitStackingOrder.remove(hand)
        explicitStackingOrder.append(hand)
    stackingOrder = map(lambda hand: 'STACKING_ORDER_%s' % (hand.upper()), explicitStackingOrder + implicitStackingOrder)
    stackingOrder.append('STACKING_ORDER_DONE')
    
    print >> config, configIn % {
        'uuId' : ', '.join(map(lambda v: '0x%02x' % v, uuid)),
        'watchName' : watchName,
        'numStepsHour' : numSteps['hour'],
        'numStepsMinute' : numSteps['minute'],
        'numStepsSecond' : numSteps['second'],
        'numStepsChronoMinute' : numSteps['chrono_minute'],
        'numStepsChronoSecond' : numSteps['chrono_second'],
        'hourHandX' : cxd.get('hour', centerX),
        'hourHandY' : cyd.get('hour', centerY),
        'minuteHandX' : cxd.get('minute', centerX),
        'minuteHandY' : cyd.get('minute', centerY),
        'secondHandX' : cxd.get('second', centerX),
        'secondHandY' : cyd.get('second', centerY),
        'chronoMinuteHandX' : cxd.get('chrono_minute', centerX),
        'chronoMinuteHandY' : cyd.get('chrono_minute', centerY),
        'chronoSecondHandX' : cxd.get('chrono_second', centerX),
        'chronoSecondHandY' : cyd.get('chrono_second', centerY),
        'compileDebugging' : int(compileDebugging),
        'showDayCard' : int(bool(dayCard)),
        'showDateCard' : int(bool(dateCard)),
        'dayCardX' : dayCard and dayCard[0],
        'dayCardY' : dayCard and dayCard[1],
        'dateCardX' : dateCard and dateCard[0],
        'dateCardY' : dateCard and dateCard[1],
        'showSecondHand' : int(showSecondHand and not suppressSecondHand),
        'enableHourBuzzer' : int(enableHourBuzzer),
        'makeChronograph' : int(makeChronograph and showChronoSecondHand),
        'showChronoMinuteHand' : int(showChronoMinuteHand),
        'showChronoSecondHand' : int(showChronoSecondHand),
        'stackingOrder' : ', '.join(stackingOrder),
        }


# Main.
try:
    opts, args = getopt.getopt(sys.argv[1:], 's:H:F:bScidl:h')
except getopt.error, msg:
    usage(1, msg)

watchStyle = None
handStyle = None
faceStyle = None
invertHands = False
compileDebugging = False
localeName = ''
for opt, arg in opts:
    if opt == '-s':
        watchStyle = arg
        if watchStyle not in watches:
            print >> sys.stderr, "Unknown watch style '%s'." % (arg)
            sys.exit(1)
    elif opt == '-H':
        handStyle = arg
        if handStyle not in hands:
            print >> sys.stderr, "Unknown hand style '%s'." % (arg)
            sys.exit(1)
    elif opt == '-F':
        faceStyle = arg
        if faceStyle not in faces:
            print >> sys.stderr, "Unknown face style '%s'." % (arg)
            sys.exit(1)
    elif opt == '-S':
        suppressSecondHand = True
    elif opt == '-b':
        enableHourBuzzer = True
    elif opt == '-c':
        makeChronograph = True
    elif opt == '-i':
        invertHands = True
    elif opt == '-d':
        compileDebugging = True
    elif opt == '-l':
        localeName = arg
    elif opt == '-h':
        usage(0)

if not watchStyle:
    print >> sys.stderr, "You must specify a desired watch style."
    sys.exit(1)

watchName, defaultHandStyle, defaultFaceStyle, uuid = watches[watchStyle]

if not handStyle:
    handStyle = defaultHandStyle
if not faceStyle:
    faceStyle = defaultFaceStyle

targetFilename, dayCard, dateCard, centers = faces[faceStyle]

locale.setlocale(locale.LC_ALL, localeName)

configWatch()
