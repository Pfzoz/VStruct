library ieee;
use ieee.std_logic_1164.all;

entity tb_mux2demux is
end entity;

architecture test of tb_mux2demux is
    component mux2demux is
        port(
            a, b : in std_logic;
            sela, selb : in std_logic;
            w, z : out std_logic
        );
    end component;
    signal a, b, sela, selb, w, z : std_logic;
begin
    u_mux2demux : mux2demux port map(a, b, sela, selb, w, z);
    p_mux2demux : process
    begin
        -- Entra B = 1 Sai 1 em W.
        a <= '0';
        b <= '1';
        sela <= '1';
        selb <= '0';
        wait for 20 ns;
    end process;
end architecture;