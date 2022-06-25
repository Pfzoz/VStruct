library ieee;
use ieee.std_logic_1164.all;

entity mux2demux is
    port(
        a, b : in std_logic;
        sela, selb : in std_logic;
        w, z : out std_logic
    );
end entity;

architecture comute of mux2demux is
    component mux2x1 is 
        port(
            a: in std_logic;
            b: in std_logic;
            sel : in std_logic;
            z : out std_logic
        );
    end component mux2x1;

    component demux2x1 is 
        port(
            e : in std_logic;
            sel : in std_logic;	
            a :  out std_logic;
            b :  out std_logic
        );
    end component demux2x1;

    signal e : std_logic;
begin
    u_mux2x1 : mux2x1 port map(a, b, sela, e);
    u_demux2x1 : demux2x1 port map(e, selb, w, z);

end architecture;