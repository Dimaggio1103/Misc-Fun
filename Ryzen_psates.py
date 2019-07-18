#!/usr/bin/python
import struct
import os
import argparse

pstates = range(0xC0010064, 0xC001006C)

def write_msr(msr, val):
    try:
        f = os.open('/dev/cpu/0/msr', os.O_WRONLY)
        os.lseek(f, msr, os.SEEK_SET)
        os.write(f, struct.pack('Q', val))
        os.close(f)
    except:
        raise OSError("msr module not loaded (run modprobe msr)")

def read_msr(msr):
    try:
        f = os.open('/dev/cpu/0/msr', os.O_RDONLY)
        os.lseek(f, msr, os.SEEK_SET)
        val = struct.unpack('Q', os.read(f, 8))[0]
        os.close(f)
        return val
    except:
        raise OSError("msr module not loaded (run modprobe msr)")

def pstate_to_str(val):
    if val & (1 << 63):
        fid = val & 0xff
        did = (val & 0x3f00) >> 8
        vid = (val & 0x3f0000) >> 14
        ratio = 25*fid/(12.5 * did)
        vcore = 1.55 - 0.00625 * vid
        return "Enabled - FID = %X - DID = %X - VID = %X - Ratio = %.2f - vCore = %.5f" % (fid, did, vid, ratio, vcore)
    else:
        return "Disabled"

def set_bits(val, base, length, new):
    return (val ^ (val & ((2 ** length - 1) << base))) + (new << base)

def set_fid(val, new):
    return set_bits(val, 0, 8, new)

def set_did(val, new):
    return set_bits(val, 8, 6, new)

def set_vid(val, new):
    return set_bits(val, 14, 8, new)

def hex(x):
    return int(x, 16)

parser = argparse.ArgumentParser(description='Sets P-States for Ryzen processors')
parser.add_argument('-l', '--list', action='store_true', help='List all P-States')
parser.add_argument('-p', '--pstate', default=-1, type=int, choices=range(8), help='P-State to set')
parser.add_argument('--enable', action='store_true', help='Enable P-State')
parser.add_argument('--disable', action='store_true', help='Disable P-State')
parser.add_argument('-f', '--fid', default=-1, type=hex, help='FID to set')
parser.add_argument('-d', '--did', default=-1, type=hex, help='DID to set')
parser.add_argument('-v', '--vid', default=-1, type=hex, help='VID to set')

args = parser.parse_args()

if args.list:
    for p in range(len(pstates)):
        print('P' + str(p) + " - " + pstate_to_str(read_msr(pstates[p])))

if args.pstate >= 0:
    new = old = read_msr(pstates[args.pstate])
    print('Current P' + str(args.pstate) + ': ' + pstate_to_str(old))
    if args.enable:
        new = set_bits(new, 63, 1, 1)
        print('Enabling state')
    if args.disable:
        new = set_bits(new, 63, 1, 0)
        print('Disabling state')
    if args.fid >= 0:
        new = set_fid(new, args.fid)
        print('Setting FID to %X' % args.fid)
    if args.did >= 0:
        new = set_did(new, args.fid)
        print('Setting DID to %X' % args.fid)
    if args.vid >= 0:
        new = set_vid(new, args.fid)
        print('Setting VID to %X' % args.fid)
    if new != old:
        print('New P' + str(args.pstate) + ': ' + pstate_to_str(new))
        write_msr(pstates[args.pstate], new)

if not args.list and args.pstate == -1:
    parser.print_help()