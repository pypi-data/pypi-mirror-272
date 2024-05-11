INDENT = 4


class Item:
    def __init__(self, name, succeed, reason) -> None:
        self.name = name
        self.succeed = succeed
        self.reason = reason
        self.children: list[Item] = []

    def __str__(self) -> str:
        return self._get_str(0)

    def _get_str(self, indent=0):
        succeed_symbol = '√' if self.succeed else '×'
        meta = not self.children

        indent_str = ' ' * indent

        if self.succeed:
            self_str = '{}{} {}'.format(indent_str, self.name, succeed_symbol)
        else:
            if meta:
                self_str = '{}{} {}: {}'.format(indent_str, self.name, succeed_symbol, self.reason)
            else:
                self_str = '{}{} {}: '.format(indent_str, self.name, succeed_symbol)

            if not meta:
                child_indent = indent + INDENT
                child_strs = [child._get_str(child_indent) for child in self.children]
                child_str = '\n'.join(child_strs)

                self_str += '\n' + child_str

        return self_str

    def append(self, child: 'Item'):
        self.children.append(child)
