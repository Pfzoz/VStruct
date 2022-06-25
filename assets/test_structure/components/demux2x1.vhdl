library ieee;
use ieee.std_logic_1164.all;

entity demux2x1 is 
    port(
        e : in std_logic;
        sel : in std_logic;	
        a :  out std_logic;
        b :  out std_logic
    );
end entity demux2x1;

architecture bhvr of demux2x1 is

    begin

    a <= e when sel = '0';
    b <= e when sel = '1';

    end architecture;
