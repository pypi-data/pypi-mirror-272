INDENT = 4
SHOW_REASON_OF_FAILURE_FOR_NON_META_ITEM = False
AUTO_CALC_SUCCEED = True


class Item:
    def __init__(self, name, succeed=False, reason='') -> None:
        self.name = name
        self._succeed = succeed
        self.reason = reason
        self.children: list[Item] = []

    @property
    def succeed(self):
        if AUTO_CALC_SUCCEED and self.children:
            return all([child.succeed for child in self.children])
        else:
            return self._succeed

    @property
    def succeed_symbol(self):
        return '√' if self.succeed else '×'

    @property
    def meta(self):
        return not self.children

    @succeed.setter
    def succeed(self, value: bool):
        self._succeed = value

    def __str__(self) -> str:
        return self._get_str(0)

    def failed_markdown(self, succeed_symbol=False):
        list_: list[str] = self._get_summaries([], succeed_symbol=succeed_symbol)
        list_ = [' - '+_s for _s in list_]
        return '\n'.join(list_)

    def _get_summaries(self, prefixs: list[str], succeed_symbol: bool = False) -> list[str]:
        def prefixed(item: Item, _prefixs: list[str]):
            result = ''
            for prefix in _prefixs:
                result += f'[{prefix}]'
            if succeed_symbol:
                result += f' {item.succeed_symbol}: {item.reason}'
            else:
                result += f' {item.reason}'
            return result

        prefixs = prefixs + [self.name]
        result = []
        for child in self.children:
            if child.meta:
                if not child.succeed:
                    result.append(prefixed(child, prefixs + [child.name]))
            else:
                result += child._get_summaries(prefixs=prefixs, succeed_symbol=succeed_symbol)
        return result

    def _get_str(self, indent=0):
        succeed_symbol = '√' if self.succeed else '×'
        meta = self.meta

        indent_str = ' ' * indent

        if self.succeed:
            self_str = '{}{} {}'.format(indent_str, self.name, succeed_symbol)
        else:
            if meta:
                self_str = '{}{} {}: {}'.format(indent_str, self.name, succeed_symbol, self.reason)
            else:
                self_str = '{}{} {}: {}'.format(indent_str, self.name, succeed_symbol, '' if not SHOW_REASON_OF_FAILURE_FOR_NON_META_ITEM else self.reason)

            if not meta:
                child_indent = indent + INDENT
                child_strs = [child._get_str(child_indent) for child in self.children]
                child_str = '\n'.join(child_strs)

                self_str += '\n' + child_str

        return self_str

    def append(self, child: 'Item'):
        self.children.append(child)
